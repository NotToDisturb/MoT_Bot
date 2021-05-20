import utils

from reaction_handlers.index_paginator_handler import IndexPaginatorHandler


class IndexPaginator:
    def __init__(self, ctx, args):
        self.ctx = ctx
        self.args = args

    async def start(self):
        if len(self.args) > 0:  # There are arguments
            if self.args[0] == "skip":  # The first argument is to be skipped
                page = 0
            elif not self.args[0].isnumeric():  # The first argument is not a number
                page = 0
                await self.do_unexpected_page(self.ctx, self.args[0], 1)
            else:
                page = int(self.args[0]) - 1
        else:
            page = 0

        if len(self.args) > 1:  # There is a second argument
            if not self.args[1].isnumeric():  # The second argument is not a number
                per_page = 10
                await self.do_unexpected_per_page(self.ctx, self.args[1], 10)
            else:
                per_page = int(self.args[1])
        else:
            per_page = 10

        pages = self.get_pages(per_page)
        # PAGE IS HIGHER THAN EXISTING PAGES
        # Show error message and exit
        if page >= pages:
            await self.do_page_too_high(self.ctx, page)
            return
        contents = self.get_page(page, per_page)

        # EVERYTHING CORRECT
        # Create embedded message and add corresponding reactions
        embed_message = self.do_embed(page, per_page, contents)
        message = await self.ctx.send(embed=embed_message)
        await self.add_reactions(message, page, per_page, pages)
        utils.get_tracker().track_message(message.id, {
            "author": self.ctx.author.id,
            "page": page,
            "per_page": per_page,
            "pages": pages,
            "reaction_handler": IndexPaginatorHandler(self.do_embed, self.get_page)
        })

    async def do_unexpected_page(self, ctx, incorrect, interpreted):
        pass

    async def do_unexpected_per_page(self, ctx, incorrect, interpreted):
        pass

    async def do_page_too_high(self, ctx, page):
        pass

    def do_embed(self, page, per_page, contents):
        pass

    def get_pages(self, per_page):
        pass

    def get_page(self, page, per_page):
        pass

    async def add_reactions(self, message, page, per_page, pages):
        pass
