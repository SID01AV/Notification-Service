from sqlalchemy.future import select
from app.utils.db_utils import Template, Database
from sqlalchemy.ext.asyncio import AsyncSession

class TemplateService:
    def __init__(self, database: Database):
        self.database = database
    
    async def get_template_by_id(self, template_id: int):
        # Create a session instance (async session)
        async for session in self.database.get_session():
            try:
                # Query the template using the given ID (async query)
                stmt = select(Template.subject, Template.body).filter(Template.template_id == template_id)
                result = await session.execute(stmt)  # Use await for async execution
                result = result.first()  # This will give you the first row (tuple) from the result

                if result:
                    # Return the result as a dictionary
                    return {"subject": result.subject, "body": result.body}
                return None
            finally:
                await session.close()  # Ensure the session is closed asynchronously

    # Method to fetch all templates
    async def get_all_templates(self):
        async for session in self.database.get_session():
            try:
                stmt = select(Template.template_id, Template.subject, Template.body)
                result = await session.execute(stmt)
                templates = result.fetchall()
                return [{"template_id": template.template_id, "subject": template.subject, "body": template.body} for template in templates]
            finally:
                await session.close()

