# from mel.parsing import Parser

# from mel.utils import Context
# from mel.exceptions import MelError, ParsingError
# from mel.exceptions.formatting import ErrorFormatter


# def parse(text, Parser=Parser):
#     try:
#         return Parser().parse()
#     except ParsingError as error:
#         message = ErrorFormatter(error).format()
#         raise MelError(message)


# def eval(text, context=Context()):
#     try:
#         tree = parse(text)
#         context.tree = tree
#         context.text = text
#         return tree
#     except MelError as error:
#         raise error
