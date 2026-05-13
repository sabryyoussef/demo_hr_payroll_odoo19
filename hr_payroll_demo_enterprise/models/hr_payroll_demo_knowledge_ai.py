import re
from html import escape

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.mail import html_to_inner_content


class HrPayrollDemoKnowledgeAsk(models.Model):
    _name = "hr.payroll.demo.knowledge.ask"
    _description = "ALLNETWORKS Knowledge AI Question"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"

    name = fields.Char(compute="_compute_name", store=True)
    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company)
    question = fields.Text(required=True, tracking=True)
    answer = fields.Html(readonly=True)
    answer_mode = fields.Selection(
        [
            ("draft", "Draft"),
            ("ai", "AI Answer"),
            ("knowledge_search", "Knowledge Search Answer"),
            ("failed", "Failed"),
        ],
        default="draft",
        tracking=True,
        readonly=True,
    )
    ai_agent_id = fields.Many2one("ai.agent", readonly=True)
    source_article_ids = fields.Many2many("knowledge.article", string="Source Articles", readonly=True)
    source_count = fields.Integer(compute="_compute_source_count")
    error_message = fields.Text(readonly=True)

    @api.depends("question")
    def _compute_name(self):
        for record in self:
            question = (record.question or "").strip().replace("\n", " ")
            record.name = question[:80] or _("Knowledge AI Question")

    @api.depends("source_article_ids")
    def _compute_source_count(self):
        for record in self:
            record.source_count = len(record.source_article_ids)

    def action_ask_ai(self):
        for record in self:
            record._answer_question()

    def action_open_sources(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Knowledge Sources"),
            "res_model": "knowledge.article",
            "view_mode": "list,form",
            "domain": [("id", "in", self.source_article_ids.ids)],
            "context": {"search_default_filter_not_is_article_item": 1},
        }

    def action_open_knowledge_root(self):
        root = self.env.ref("hr_payroll_demo_enterprise.knowledge_root_employee_handbook", raise_if_not_found=False)
        if not root:
            raise UserError(_("The ALLNETWORKS Knowledge base was not found."))
        return {
            "type": "ir.actions.act_window",
            "name": root.display_name,
            "res_model": "knowledge.article",
            "res_id": root.id,
            "view_mode": "form",
            "target": "current",
        }

    def action_open_ai_agent(self):
        agent = self.env.ref("hr_payroll_demo_enterprise.ai_agent_allnetworks_knowledge", raise_if_not_found=False)
        if not agent:
            raise UserError(_("The ALLNETWORKS Knowledge AI agent was not found."))
        return {
            "type": "ir.actions.act_window",
            "name": agent.display_name,
            "res_model": "ai.agent",
            "res_id": agent.id,
            "view_mode": "form",
            "target": "current",
        }

    def _answer_question(self):
        self.ensure_one()
        if not self.question or not self.question.strip():
            raise UserError(_("Type a question first."))

        source_articles = self._find_relevant_articles(self.question)
        context_message = self._build_context_message(source_articles)
        agent = self.env.ref("hr_payroll_demo_enterprise.ai_agent_allnetworks_knowledge", raise_if_not_found=False)

        if agent:
            try:
                response = agent.get_direct_response(
                    prompt=self.question,
                    context_message=context_message,
                    enable_html_response=True,
                )
                answer = "".join(response) if isinstance(response, list) else str(response)
                self.write(
                    {
                        "answer": answer or self._build_fallback_answer(source_articles),
                        "answer_mode": "ai",
                        "ai_agent_id": agent.id,
                        "source_article_ids": [(6, 0, source_articles.ids)],
                        "error_message": False,
                    }
                )
                return
            except Exception as exc:
                # Demo environments may not have a live AI provider token. The fallback still answers from Knowledge.
                self.write({"error_message": str(exc)})

        self.write(
            {
                "answer": self._build_fallback_answer(source_articles),
                "answer_mode": "knowledge_search" if source_articles else "failed",
                "ai_agent_id": agent.id if agent else False,
                "source_article_ids": [(6, 0, source_articles.ids)],
            }
        )

    def _knowledge_domain(self):
        root = self.env.ref("hr_payroll_demo_enterprise.knowledge_root_employee_handbook", raise_if_not_found=False)
        if root:
            return [("id", "child_of", root.id), ("is_template", "=", False)]
        return [("name", "ilike", "ALLNETWORKS"), ("is_template", "=", False)]

    def _find_relevant_articles(self, question, limit=5):
        Article = self.env["knowledge.article"].sudo()
        articles = Article.search(self._knowledge_domain())
        terms = [term for term in re.findall(r"[A-Za-z0-9]+", question.lower()) if len(term) > 2]
        if not terms:
            return articles[:limit]

        scored = []
        for article in articles:
            text = self._article_plain_text(article).lower()
            score = sum(text.count(term) for term in terms)
            if score:
                scored.append((score, article.id))
        scored.sort(reverse=True)
        return Article.browse([article_id for _score, article_id in scored[:limit]])

    def _article_plain_text(self, article):
        body = html_to_inner_content(article.body or "")
        return f"{article.name or ''}\n{body or ''}"

    def _build_context_message(self, articles):
        if not articles:
            return "No matching ALLNETWORKS Knowledge articles were found."
        chunks = []
        for article in articles:
            chunks.append(
                "Article: %s\nURL: %s\nContent:\n%s"
                % (article.display_name, article.article_url or "", self._article_plain_text(article)[:2500])
            )
        return (
            "Answer only from these ALLNETWORKS Knowledge articles. "
            "If the answer is not covered, say which HR/Payroll/Finance team should be contacted.\n\n"
            + "\n\n---\n\n".join(chunks)
        )

    def _build_fallback_answer(self, articles):
        if not articles:
            return _(
                "<p>No matching Knowledge article was found. Try asking about payroll, leave, attendance, expenses, "
                "training, bank payment, holidays, overtime, or company policy.</p>"
            )

        parts = [
            "<p><strong>Knowledge answer based on ALLNETWORKS articles.</strong></p>",
            "<p>The live AI provider was not available or not configured, so this answer uses the closest Knowledge articles.</p>",
        ]
        for article in articles:
            text = escape(self._article_plain_text(article)[:900])
            url = article.article_url or "#"
            parts.append(
                "<h3>%s</h3><p>%s%s</p><p><a href=\"%s\" target=\"_blank\">Open Knowledge article</a></p>"
                % (escape(article.display_name), text, "..." if len(text) >= 900 else "", escape(url))
            )
        return "".join(parts)
