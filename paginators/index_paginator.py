import utils

from paginators.paginator import Paginator
from reaction_handlers.index_paginator_handler import IndexPaginatorHandler


class IndexPaginator(Paginator):
    def __init__(self, ctx, args, per_page=-1):
        self.ctx = ctx
        self.args = args
        self.per_page = per_page

    async def get_page(self):
        if len(self.args) > 0:  # There are arguments
            if self.args[0] == "skip":  # The first argument is to be skipped
                return 0
            elif not self.args[0].isnumeric() \
                    or int(self.args[0]) - 1 < 0:  # The first argument is not a number
                await self.do_unexpected_page(self.ctx, self.args[0], 1)
                return 0
            else:
                return int(self.args[0]) - 1
        else:
            return 0

    async def get_per_page(self):
        if self.per_page > -1:
            return self.per_page
        else:
            if len(self.args) > 1:  # There is a second argument
                if not self.args[1].isnumeric() \
                        or int(self.args[1]) - 1 < 0:  # The second argument is not a number
                    await self.do_unexpected_per_page(self.ctx, self.args[1], 10)
                    return 10
                else:
                    return int(self.args[1])
            else:
                return 10

    async def do_page_validity(self, page, pages):
        if page >= pages:
            await self.do_page_too_high(page)
            return False
        return True

    def build_embed(self, page, per_page):
        contents = self.get_page_contents(page, per_page)
        return self.do_embed(page, per_page, contents)

    def track_message(self, message, page, per_page, pages):
        utils.get_tracker().track_message(message.id, {
            "author": self.ctx.author.id,
            "page": page,
            "per_page": per_page,
            "pages": pages,
            "reaction_handler": IndexPaginatorHandler(self.build_embed)
        })
