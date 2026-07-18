from pygments.lexer import RegexLexer

from pygments.token import Number, String, Keyword, Comment, Name, Operator, Punctuation, Text



class PytLexer(RegexLexer):

    # // _________________________________________________________________________________________________

    float_lex = r'\b\d+\.\d+\b'
    int_lex = r'\b\d+\b'

    # // ___________________________________

    str_m_lex = r"'[^']*'"
    str_d_lex = r'"[^"]*"'

    # // ___________________________________

    func_lex = r'\b(abs|aiter|all|anext|any|ascii|bin|bool|breakpoint|bytearray|bytes|callable|chr|classmethod|compile|complex|copyright|credits|delattr|dict|dir|divmod|enumerate|eval|exec|exit|filter|float|format|frozenset|getattr|globals|hasattr|hash|help|hex|id|input|int|isinstance|issubclass|iter|len|license|list|locals|map|max|memoryview|min|next|object|oct|open|ord|pow|print|property|quit|range|repr|reversed|round|set|setattr|slice|sorted|staticmethod|str|sum|super|tuple|type|vars|zip)\b'
    other_lex = r'.'
    prefix_lex = r'\b(_sh_|_pyt_|_\._|_pyt\+\+_|_pyt-eval_|_pyt-exec_|_&_|_\?_)\b'
    except_lex = r'\b(TypeError|EOFError|KeyboardInterrupt|ArithmeticError|AssertionError|AttributeError|BaseException|BaseExceptionGroup|BlockingIOError|BrokenPipeError|BufferError|ChildProcessError|ConnectionAbortedError|ConnectionError|ConnectionRefusedError|ConnectionResetError|EOFError|EnvironmentError|Exception|ExceptionGroup|FileExistsError|FileNotFoundError|FloatingPointError|IOError|ImportError|IndentationError|IndexError|InterruptedError|IsADirectoryError|KeyError|LookupError|MemoryError|ModuleNotFoundError|NameError|NotADirectoryError|NotImplementedError|OSError|OverflowError|PermissionError|ProcessLookupError|PythonFinalizationError|RecursionError|ReferenceError|RuntimeError|SyntaxError|SystemError|TabError|TimeoutError|TypeError|UnboundLocalError|UnicodeDecodeError|UnicodeEncodeError|UnicodeError|UnicodeTranslateError|ValueError|WindowsError|ZeroDivisionError|_IncompleteInputError)\b'
    keyword_lex = r'\b(False|None|True|and|as|assert|async|await|break|class|continue|del|elif|else|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)\b'
    name_lex = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'
    decorator_lex = r'(@.*$)'

    # // _________________________________________________________________________________________________

    name = 'simple_shell'
    aliases = ['simple_shell']

    tokens = {
        "root": [

            (prefix_lex, Name.Prefix),

            (int_lex, Number),
            (float_lex, Number),

            (str_d_lex, String),
            (str_m_lex, String),

            # keyword
            (keyword_lex, Keyword),

            (func_lex, Name.Action),
            (decorator_lex, Name.Action),
            (r'\b(def)\b', Keyword,'def_name'),
            (r'\b(class)\b', Keyword, 'def_name'),

            (r'\b(except)\b', Keyword, 'except_name'),

            # name
            (name_lex, Name),
            (r'_#_[^\n]*', Comment),

            (r'(//.*$|#.*$)', Comment, 'comment_name'),


            # operators
            (r'[=+\-*/<>!]+', Operator),

            # punctuation
            (r'[{}()\[\],.]', Punctuation),

            # space
            (r'\s+', Text),

            # other
            (other_lex, Text),
        ],
        'def_name':[
            (r'\s+', Text),
            (func_lex, Name.Error),
            (name_lex, Name.Defer, 'root'),
            (r'[()]', Name.Error, "root"),
            (other_lex, Name.Error)
        ],
        'except_name':[
            (except_lex, Name.Action, 'root'),
            (r':', Punctuation, 'root'),
            (r'[()]', Punctuation),
            (r',', Punctuation, 'except_name'),
            (r'\w+', Punctuation),
            (r'\s+', Text),

            (other_lex, Name.Error)
        ],
        'comment_name':[
            (r'\b(_&_)\b', Name.Prefix, 'root'),
            (other_lex, Comment),
        ]
    }




