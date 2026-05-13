"""
Pre-migration for hr_payroll_demo_enterprise 19.0.1.0.1

ai_agent_id was changed from Many2one("ai.agent") (integer FK) to Char.
PostgreSQL cannot alter the column type while the FK constraint exists,
so we drop it here before Odoo's _auto_init converts the column to varchar.

Uses DO $$ EXCEPTION to stay safe when:
- the table was never created (fresh Odoo.sh DB without ai.agent module)
- the constraint was already dropped by a previous migration attempt
"""


def migrate(cr, version):
    cr.execute(
        """
        DO $$
        BEGIN
            ALTER TABLE hr_payroll_demo_knowledge_ask
                DROP CONSTRAINT IF EXISTS
                hr_payroll_demo_knowledge_ask_ai_agent_id_fkey;
        EXCEPTION
            WHEN undefined_table THEN NULL;
        END $$
        """
    )
