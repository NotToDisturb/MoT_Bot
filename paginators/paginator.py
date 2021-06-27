import utils


class Paginator:
    def __init__(self, ctx, args):
        self.ctx = ctx
        self.args = args

    async def start(self):
        self.do_incorrect_usage_check()
        page = await self.get_page()
        per_page = await self.get_per_page()
        pages = self.get_pages(page, per_page)

        # PAGE IS HIGHER THAN EXISTING PAGES
        # Show error message and exit
        if not await self.do_page_validity(page, pages):
            return

        # EVERYTHING CORRECT
        # Create embedded message and add corresponding reactions
        embed_message = self.build_embed(page, per_page)
        message = await self.ctx.send(embed=embed_message)
        await self.add_reactions(message, page, per_page, pages)
        self.track_message(message, page, per_page, pages)

    def do_incorrect_usage_check(self):
        return

    async def do_unexpected_page(self, incorrect, interpreted):
        pass

    async def do_unexpected_per_page(self, incorrect, interpreted):
        pass

    async def do_page_too_high(self, page):
        pass

    def build_embed(self, page, per_page):
        pass

    def do_embed(self, page, per_page, contents):
        pass

    async def get_page(self):
        pass

    async def get_per_page(self):
        pass

    async def do_page_validity(self, page, pages):
        pass

    def get_pages(self, page, per_page):
        pass

    def get_page_contents(self, page, per_page):
        pass

    async def add_reactions(self, message, page, per_page, pages):
        await message.add_reaction("◀️")
        await message.add_reaction("▶️")
        await message.add_reaction("🗑️")

    def track_message(self, message, page, per_page, pages):
        pass
