class TextManager:
    @staticmethod
    def compile_lines(text_generator, codeblock=False, diff=False):
        """Join lines that are separated by a new line."""
        text = '\n'.join([x for x in text_generator])
        if codeblock:
            text = TextManager.add_codeblock(text, diff=diff)
        return text

    @staticmethod
    def add_codeblock(text, diff=False):
        if diff:
            return '\n'.join(['```diff', text, '```'])

        return '\n'.join(['```', text, '```'])

    @staticmethod
    def compile_msg_blocks(*args):
        """Allows for the conjunction of various `compile_lines`.

        Parameters are a series of (text_generator/text, codeblock_bool).
        """
        return_str = ""

        for text, codeblock_bool in args:
            if isinstance(text, str):
                if codeblock_bool is True:
                    block_to_add = TextManager.add_codeblock(text)
                else:
                    block_to_add = text
            else:  # Text is a generator
                block_to_add = TextManager.compile_lines(
                    text, codeblock=codeblock_bool
                )
            return_str = '\n'.join([return_str, block_to_add])

        return_str = return_str.replace('\n', '', 1)  # Remove first \n
        return return_str

    @staticmethod
    async def send_msg_blocks(ctx, *args):
        """Compiles message blocks and sends them.

        `*args` are a series of (text_generator/text, codeblock_bool).
        """
        await ctx.send(TextManager.compile_msg_blocks(*args))
