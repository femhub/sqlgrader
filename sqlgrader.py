import copy
import itertools
import operator
import random
import re
import string
from collections import Counter as c

import sqlparse

############
# KEYWORDS #
############


# 'AS' keyword is not included in the 'first' category of keywords!
# The reason for this is that it is not necessary to use it in some cases
# to correctly solve a level. The same holds for inequalities.
sql_reserved = [
    "ABS",
    "ABSOLUTE",
    "ACCESS",
    "ACTION",
    "ADD",
    "ADMIN",
    "AFTER",
    "ALIAS",
    "ALL",
    "ALTER",
    "AND",
    "ANY",
    "ARE",
    "ARRAY",
    "ASC",
    "ASSIGNMENT",
    "AT",
    "ATTRIBUTE",
    "ATTRIBUTES",
    "AUTHORIZATION",
    "AUTO_INCREMENT",
    "AVG",
    "BACKUP",
    "BACKWARD",
    "BEFORE",
    "BEGIN",
    "BETWEEN",
    "BIGINT",
    "BINARY",
    "BLOB",
    "BOOL",
    "BOOLEAN",
    "BOTH",
    "BREAK",
    "BROWSE",
    "BULK",
    "BY",
    "CACHE",
    "CASCADE",
    "CASCADED",
    "CASE",
    "CEIL",
    "CEILING",
    "CHAIN",
    "CHANGE",
    "CHAR",
    "CHAR_LENGTH",
    "CHARACTER",
    "CHARACTER_LENGTH",
    "CHARACTER_SET_CATALOG",
    "CHARACTER_SET_NAME",
    "CHARACTER_SET_SCHEMA",
    "CHARACTERISTICS",
    "CHARACTERS",
    "CHECK",
    "CHECKED",
    "CHECKPOINT",
    "CHECKSUM",
    "CLASS",
    "CLASS_ORIGIN",
    "CLOB",
    "CLOSE",
    "CLUSTER",
    "CLUSTERED",
    "COALESCE",
    "COBOL",
    "COLLATE",
    "COLLATION",
    "COLLATION_CATALOG",
    "COLLATION_NAME",
    "COLLATION_SCHEMA",
    "COLLECT",
    "COLUMN",
    "COLUMN_NAME",
    "COLUMNS",
    "COMMAND_FUNCTION",
    "COMMAND_FUNCTION_CODE",
    "COMMENT",
    "COMMIT",
    "COMMITTED",
    "COMPLETION",
    "COMPRESS",
    "COMPUTE",
    "CONCAT",
    "CONDITION",
    "CONDITION_NUMBER",
    "CONNECT",
    "CONNECTION",
    "CONNECTION_NAME",
    "CONSTRAINT",
    "CONSTRAINT_CATALOG",
    "CONSTRAINT_NAME",
    "CONSTRAINT_SCHEMA",
    "CONSTRAINTS",
    "CONSTRUCTOR",
    "CONTAINS",
    "CONTAINSTABLE",
    "CONTINUE",
    "CONVERSION",
    "CONVERT",
    "COPY",
    "CORR",
    "CORRESPONDING",
    "COUNT",
    "COVAR_POP",
    "COVAR_SAMP",
    "CREATE",
    "CREATEDB",
    "CREATEROLE",
    "CREATEUSER",
    "CROSS",
    "CSV",
    "CUBE",
    "CUME_DIST",
    "CURRENT",
    "CURRENT_DATE",
    "CURRENT_DEFAULT_TRANSFORM_GROUP",
    "CURRENT_PATH",
    "CURRENT_ROLE",
    "CURRENT_TIME",
    "CURRENT_TIMESTAMP",
    "CURRENT_TRANSFORM_GROUP_FOR_TYPE",
    "CURRENT_USER",
    "CURSOR",
    "CURSOR_NAME",
    "CYCLE",
    "DATA",
    "DATABASE",
    "DATABASES",
    "DATE",
    "DATETIME",
    "DATETIME_INTERVAL_CODE",
    "DATETIME_INTERVAL_PRECISION",
    "DAY",
    "DAY_HOUR",
    "DAY_MICROSECOND",
    "DAY_MINUTE",
    "DAY_SECOND",
    "DAYOFMONTH",
    "DAYOFWEEK",
    "DAYOFYEAR",
    "DBCC",
    "DEALLOCATE",
    "DEC",
    "DECIMAL",
    "DECLARE",
    "DEFAULT",
    "DEFAULTS",
    "DEFERRABLE",
    "DEFERRED",
    "DEFINED",
    "DEFINER",
    "DEGREE",
    "DELAY_KEY_WRITE",
    "DELAYED",
    "DELETE",
    "DELIMITER",
    "DELIMITERS",
    "DENSE_RANK",
    "DENY",
    "DEPTH",
    "DEREF",
    "DERIVED",
    "DESC",
    "DESCRIBE",
    "DESCRIPTOR",
    "DESTROY",
    "DESTRUCTOR",
    "DETERMINISTIC",
    "DIAGNOSTICS",
    "DICTIONARY",
    "DISABLE",
    "DISCONNECT",
    "DISK",
    "DISPATCH",
    "DISTINCT",
    "DISTINCTROW",
    "DISTRIBUTED",
    "DIV",
    "DO",
    "DOMAIN",
    "DOUBLE",
    "DROP",
    "DUAL",
    "DUMMY",
    "DUMP",
    "DYNAMIC",
    "DYNAMIC_FUNCTION",
    "DYNAMIC_FUNCTION_CODE",
    "EACH",
    "ELEMENT",
    "ELSE",
    "ELSEIF",
    "ENABLE",
    "ENCLOSED",
    "ENCODING",
    "ENCRYPTED",
    "END",
    "END-EXEC",
    "ENUM",
    "EQUALS",
    "ERRLVL",
    "ESCAPE",
    "ESCAPED",
    "EVERY",
    "EXCEPT",
    "EXCEPTION",
    "EXCLUDE",
    "EXCLUDING",
    "EXCLUSIVE",
    "EXEC",
    "EXECUTE",
    "EXISTING",
    "EXISTS",
    "EXIT",
    "EXP",
    "EXPLAIN",
    "EXTERNAL",
    "EXTRACT",
    "FALSE",
    "FETCH",
    "FIELDS",
    "FILE",
    "FILLFACTOR",
    "FILTER",
    "FINAL",
    "FIRST",
    "FLOAT",
    "FLOAT4",
    "FLOAT8",
    "FLOOR",
    "FLUSH",
    "FOLLOWING",
    "FOR",
    "FORCE",
    "FOREIGN",
    "FORTRAN",
    "FORWARD",
    "FOUND",
    "FREE",
    "FREETEXT",
    "FREETEXTTABLE",
    "FREEZE",
    "FROM",
    "FULL",
    "FULLTEXT",
    "FUNCTION",
    "FUSION",
    "G",
    "GENERAL",
    "GENERATED",
    "GET",
    "GLOBAL",
    "GO",
    "GOTO",
    "GRANT",
    "GRANTED",
    "GRANTS",
    "GREATEST",
    "GROUP",
    "GROUPBY",
    "GROUP BY",
    "GROUPING",
    "HANDLER",
    "HAVING",
    "HEADER",
    "HEAP",
    "HIERARCHY",
    "HIGH_PRIORITY",
    "HOLD",
    "HOLDLOCK",
    "HOST",
    "HOSTS",
    "HOUR",
    "HOUR_MICROSECOND",
    "HOUR_MINUTE",
    "HOUR_SECOND",
    "IDENTIFIED",
    "IDENTITY",
    "IF",
    "IGNORE",
    "ILIKE",
    "IMMEDIATE",
    "IMMUTABLE",
    "IMPLEMENTATION",
    "IMPLICIT",
    "IN",
    "INCLUDE",
    "INCLUDING",
    "INCREMENT",
    "INDEX",
    "INDICATOR",
    "INFILE",
    "INFIX",
    "INHERIT",
    "INHERITS",
    "INITIAL",
    "INITIALIZE",
    "INITIALLY",
    "INNER",
    "INOUT",
    "INPUT",
    "INSENSITIVE",
    "INSERT",
    "INSERT_ID",
    "INSTANCE",
    "INSTANTIABLE",
    "INSTEAD",
    "INT",
    "INT1",
    "INT2",
    "INT3",
    "INT4",
    "INT8",
    "INTEGER",
    "INTERSECT",
    "INTERSECTION",
    "INTERVAL",
    "INTO",
    "INVOKER",
    "IS",
    "ISAM",
    "ISNULL",
    "ISOLATION",
    "ITERATE",
    "JOIN",
    "KEY",
    "KEY_MEMBER",
    "KEY_TYPE",
    "KEYS",
    "KILL",
    "LANCOMPILER",
    "LANGUAGE",
    "LARGE",
    "LAST",
    "LAST_INSERT_ID",
    "LATERAL",
    "LEADING",
    "LEAST",
    "LEAVE",
    "LEFT",
    "LENGTH",
    "LESS",
    "LEVEL",
    "LIKE",
    "LIMIT",
    "LINENO",
    "LINES",
    "LISTEN",
    "LN",
    "LOAD",
    "LOCAL",
    "LOCALTIME",
    "LOCALTIMESTAMP",
    "LOCATION",
    "LOCATOR",
    "LOCK",
    "LOGIN",
    "LOGS",
    "LONG",
    "LONGBLOB",
    "LONGTEXT",
    "LOOP",
    "LOW_PRIORITY",
    "LOWER",
    "M",
    "MAP",
    "MATCH",
    "MATCHED",
    "MAX",
    "MAX_ROWS",
    "MAXVALUE",
    "MEDIUMBLOB",
    "MEDIUMINT",
    "MEDIUMTEXT",
    "MEMBER",
    "MERGE",
    "MESSAGE_LENGTH",
    "MESSAGE_OCTET_LENGTH",
    "MESSAGE_TEXT",
    "METHOD",
    "MIDDLEINT",
    "MIN",
    "MIN_ROWS",
    "MINUS",
    "MINUTE",
    "MINUTE_MICROSECOND",
    "MINUTE_SECOND",
    "MINVALUE",
    "MLSLABEL",
    "MOD",
    "MODE",
    "MODIFIES",
    "MODIFY",
    "MODULE",
    "MONTH",
    "MONTHNAME",
    "MORE",
    "MOVE",
    "MULTISET",
    "MUMPS",
    "MYISAM",
    "NAMES",
    "NATIONAL",
    "NATURAL",
    "NCHAR",
    "NCLOB",
    "NESTING",
    "NEW",
    "NEXT",
    "NO",
    "NO_WRITE_TO_BINLOG",
    "NOAUDIT",
    "NOCHECK",
    "NOCOMPRESS",
    "NOCREATEDB",
    "NOCREATEROLE",
    "NOCREATEUSER",
    "NOINHERIT",
    "NOLOGIN",
    "NONCLUSTERED",
    "NONE",
    "NORMALIZE",
    "NORMALIZED",
    "NOSUPERUSER",
    "NOT",
    "NOTHING",
    "NOTIFY",
    "NOTNULL",
    "NOWAIT",
    "NULL",
    "NULLABLE",
    "NULLIF",
    "NULLS",
    "NUMBER",
    "NUMERIC",
    "OBJECT",
    "OCTET_LENGTH",
    "OCTETS",
    "OF",
    "OFF",
    "OFFLINE",
    "OFFSET",
    "OFFSETS",
    "OIDS",
    "OLD",
    "ON",
    "ONLINE",
    "ONLY",
    "OPEN",
    "OPENDATASOURCE",
    "OPENQUERY",
    "OPENROWSET",
    "OPENXML",
    "OPERATION",
    "OPERATOR",
    "OPTIMIZE",
    "OPTION",
    "OPTIONALLY",
    "OPTIONS",
    "OR",
    "ORDER",
    "ORDERBY",
    "ORDER BY",
    "ORDERING",
    "ORDINALITY",
    "OTHERS",
    "OUT",
    "OUTER",
    "OUTFILE",
    "OUTPUT",
    "OVER",
    "OVERLAPS",
    "OVERLAY",
    "OVERRIDING",
    "OWNER",
    "PACK_KEYS",
    "PAD",
    "PARAMETER",
    "PARAMETER_MODE",
    "PARAMETER_NAME",
    "PARAMETER_ORDINAL_POSITION",
    "PARAMETER_SPECIFIC_CATALOG",
    "PARAMETER_SPECIFIC_NAME",
    "PARAMETER_SPECIFIC_SCHEMA",
    "PARAMETERS",
    "PARTIAL",
    "PARTITION",
    "PASCAL",
    "PASSWORD",
    "PATH",
    "PCTFREE",
    "PERCENT",
    "PERCENT_RANK",
    "PERCENTILE_CONT",
    "PERCENTILE_DISC",
    "PLACING",
    "PLAN",
    "PLI",
    "POSITION",
    "POSTFIX",
    "POWER",
    "PRECEDING",
    "PRECISION",
    "PREFIX",
    "PREORDER",
    "PREPARE",
    "PREPARED",
    "PRESERVE",
    "PRIMARY",
    "PRINT",
    "PRIOR",
    "PRIVILEGES",
    "PROC",
    "PROCEDURAL",
    "PROCEDURE",
    "PROCESS",
    "PROCESSLIST",
    "PUBLIC",
    "PURGE",
    "QUOTE",
    "RAID0",
    "RAISERROR",
    "RANGE",
    "RANK",
    "RAW",
    "READ",
    "READS",
    "READTEXT",
    "REAL",
    "RECHECK",
    "RECONFIGURE",
    "RECURSIVE",
    "REF",
    "REFERENCES",
    "REFERENCING",
    "REGEXP",
    "REGR_AVGX",
    "REGR_AVGY",
    "REGR_COUNT",
    "REGR_INTERCEPT",
    "REGR_R2",
    "REGR_SLOPE",
    "REGR_SXX",
    "REGR_SXY",
    "REGR_SYY",
    "REINDEX",
    "RELATIVE",
    "RELEASE",
    "RELOAD",
    "RENAME",
    "REPEAT",
    "REPEATABLE",
    "REPLACE",
    "REPLICATION",
    "REQUIRE",
    "RESET",
    "RESIGNAL",
    "RESOURCE",
    "RESTART",
    "RESTORE",
    "RESTRICT",
    "RESULT",
    "RETURN",
    "RETURNED_CARDINALITY",
    "RETURNED_LENGTH",
    "RETURNED_OCTET_LENGTH",
    "RETURNED_SQLSTATE",
    "RETURNS",
    "REVOKE",
    "RIGHT",
    "RLIKE",
    "ROLE",
    "ROLLBACK",
    "ROLLUP",
    "ROUND",
    "ROUTINE",
    "ROUTINE_CATALOG",
    "ROUTINE_NAME",
    "ROUTINE_SCHEMA",
    "ROW",
    "ROW_COUNT",
    "ROW_NUMBER",
    "ROWCOUNT",
    "ROWGUIDCOL",
    "ROWID",
    "ROWNUM",
    "ROWS",
    "RULE",
    "SAVE",
    "SAVEPOINT",
    "SCALE",
    "SCHEMA",
    "SCHEMA_NAME",
    "SCHEMAS",
    "SCOPE",
    "SCOPE_CATALOG",
    "SCOPE_NAME",
    "SCOPE_SCHEMA",
    "SCROLL",
    "SEARCH",
    "SECOND",
    "SECOND_MICROSECOND",
    "SECTION",
    "SECURITY",
    "SELECT",
    "SELF",
    "SENSITIVE",
    "SEPARATOR",
    "SEQUENCE",
    "SERIALIZABLE",
    "SERVER_NAME",
    "SESSION",
    "SESSION_USER",
    "SET",
    "SETOF",
    "SETS",
    "SETUSER",
    "SHARE",
    "SHOW",
    "SHUTDOWN",
    "SIGNAL",
    "SIMILAR",
    "SIMPLE",
    "SIZE",
    "SMALLINT",
    "SOME",
    "SONAME",
    "SOURCE",
    "SPACE",
    "SPATIAL",
    "SPECIFIC",
    "SPECIFIC_NAME",
    "SPECIFICTYPE",
    "SQL",
    "SQRT",
    "START",
    "STARTING",
    "STATE",
    "STATEMENT",
    "STATIC",
    "STATISTICS",
    "STATUS",
    "STDDEV_POP",
    "STDDEV_SAMP",
    "STDIN",
    "STDOUT",
    "STORAGE",
    "STRAIGHT_JOIN",
    "STRICT",
    "STRING",
    "STRUCTURE",
    "STYLE",
    "SUBCLASS_ORIGIN",
    "SUBLIST",
    "SUBMULTISET",
    "SUBSTRING",
    "SUCCESSFUL",
    "SUM",
    "SUPERUSER",
    "SYMMETRIC",
    "SYNONYM",
    "SYSDATE",
    "SYSID",
    "SYSTEM",
    "SYSTEM_USER",
    "TABLE",
    "TABLE_NAME",
    "TABLES",
    "TABLESAMPLE",
    "TABLESPACE",
    "TEMP",
    "TEMPLATE",
    "TEMPORARY",
    "TERMINATE",
    "TERMINATED",
    "TEXT",
    "TEXTSIZE",
    "THAN",
    "THEN",
    "TIES",
    "TIME",
    "TIMESTAMP",
    "TIMEZONE_HOUR",
    "TIMEZONE_MINUTE",
    "TINYBLOB",
    "TINYINT",
    "TINYTEXT",
    "TO",
    "TOAST",
    "TOP",
    "TOP_LEVEL_COUNT",
    "TRAILING",
    "TRAN",
    "TRANSACTION",
    "TRANSACTION_ACTIVE",
    "TRANSACTIONS_COMMITTED",
    "TRANSACTIONS_ROLLED_BACK",
    "TRANSFORM",
    "TRANSFORMS",
    "TRANSLATE",
    "TRANSLATION",
    "TREAT",
    "TRIGGER",
    "TRIM",
    "TRUE",
    "TRUNCATE",
    "TRUSTED",
    "TSEQUAL",
    "TYPE",
    "UESCAPE",
    "UID",
    "UNBOUNDED",
    "UNCOMMITTED",
    "UNDER",
    "UNDO",
    "UNENCRYPTED",
    "UNION",
    "UNIQUE",
    "UNKNOWN",
    "UNLISTEN",
    "UNLOCK",
    "UNNAMED",
    "UNNEST",
    "UNSIGNED",
    "UNTIL",
    "UPDATE",
    "UPDATETEXT",
    "UPPER",
    "USAGE",
    "USE",
    "USER",
    "USER_DEFINED_TYPE_CATALOG",
    "USER_DEFINED_TYPE_CODE",
    "USER_DEFINED_TYPE_NAME",
    "USER_DEFINED_TYPE_SCHEMA",
    "USING",
    "UTC_DATE",
    "UTC_TIME",
    "UTC_TIMESTAMP",
    "VACUUM",
    "VALID",
    "VALIDATE",
    "VALIDATOR",
    "VALUE",
    "VALUES",
    "VAR_SAMP",
    "VARBINARY",
    "VARCHAR",
    "VARCHAR2",
    "VARCHARACTER",
    "VARIABLE",
    "VARIABLES",
    "VARYING",
    "VERBOSE",
    "VIEW",
    "WHEN",
    "WHERE",
    "WHILE",
    "WINDOW",
    "WITH",
    "WITHIN",
    "WITHOUT",
    "WORK",
    "WRITE",
    "XOR",
    "YEAR",
    "YEAR_MONTH",
    "ZEROFILL",
    "ZONE",
]

# List of SQL words which are not always necessary to resolve a particular task, second category words
sql_reserved_2 = ["<", ">", "<=", ">=", "=", "<>", "!="]

# List of aggregate functions
sql_aggregate = ["AVG", "COUNT", "MAX", "MIN", "SUM"]


#############################
# AUXILIARY GLOBAL SETTINGS #
#############################


# Sqlparse keyword tokens
sqlparse_keyword_t = [
    sqlparse.tokens.Keyword,
    sqlparse.tokens.Keyword.DDL,
    sqlparse.tokens.Keyword.DML,
    sqlparse.tokens.Keyword.CTE,
]

# Sqlparse whitespace tokens
sqlparse_whitespace_t = [sqlparse.tokens.Whitespace, sqlparse.tokens.Whitespace.Newline]

# Dictionary of per-table-column parameters which we grade, togther with a human-readable explanation
table_columns_check = {
    "column_name": "column name",
    "data_type": "data type",
    "character_maximum_length": "character maximum length",
    "is_nullable": "nullability",
    "column_default": "default value",
}


#######################
# AUXILIARY FUNCTIONS #
#######################


def isListEmpty(inList):
    if isinstance(inList, list):  # Is a list
        return all(map(isListEmpty, inList))
    return False  # Not a list


def sql_clean_and_divide(code):
    """Cleans all comments and divides the SQL code according to statements using sqlparse library
    :param code:
    SQL code to cleaned and divided
    :return:
    list - list of cleaned and well-formated SQL commands
    """

    cleaned_code = sqlparse.format(code, strip_comments=True).strip()
    return sqlparse.parse(cleaned_code)


def sql_replace(st, old, new):
    """Replaces a token in a sqlparse statement
    :param st:
    Sqlparse statement
    :old:
    Value to be replaced
    :new:
    New value
    :return:
    Sqlparse statement
    """

    st = str(st)
    old = str(old)
    new = str(new)

    sql_code = re.sub(
        r"(?<=[^0-9a-zA-Z_])%s(?=[^0-9a-zA-Z_])" % old, new, st, flags=re.IGNORECASE
    )

    return sqlparse.parse(sql_code)[0]


def sql_code_sanitizer(sql):
    """Serves to get list of SQL keywords and values from a SQL command
    :param sql:
    SQL string
    :returns:
    sql_l - list of SQL keywords, order is preserved
    """

    # First we get rid of strings between quotations, then we normalize spaces
    strings_re = re.compile("'((?:[^']|\\.|'')*)'")
    strings = re.findall(strings_re, sql)
    sql_normalized = re.sub(strings_re, " -- ", sql)
    sql_normalized = re.sub(r"\s+", " ", sql_normalized)

    # List of auxiliary substitutes for keywords made up of more words
    k = [
        ["GROUP BY", "GROUPBY"],
        ["ORDER BY", "ORDERBY"],
        ["SIMILAR TO", "SIMILARTO"],
        ["IF EXISTS", "IFEXISTS"],
    ]

    # Replace keywords from k before splitting
    sub_keywords = lambda s, k: re.sub("(?i)" + re.escape(k[0]), k[1], s)
    for i in k:
        sql_normalized = sub_keywords(sql_normalized, i)

    # Splitting the output string
    sql_l = re.split(r"[\s.,();]+", sql_normalized)
    while "" in sql_l:
        sql_l.remove("")

    # Return to the proper form of double keywords
    sub_keywords_back = lambda l, k: [x if x != k[1] else k[0] for x in l]
    for i in k:
        sql_l = sub_keywords_back(sql_l, i)
    for i in strings:
        sql_l[sql_l.index("--")] = "'" + i + "'"
        # Quotations are added back as they are defacto a part of the statement

    return sql_l


def sql_code_simplifier(sql_l):
    arbitrary_words = ["as"]
    keywords_dict = {}
    sql_l_ordinal = []
    next = False
    for i in sql_l:
        if i in keywords_dict:
            keywords_dict[i] += 1
        else:
            keywords_dict[i] = 1
        if i.lower() == "as":
            next = True
        else:
            if next == True:
                arbitrary_words.append(i.lower())
            next = False
        sql_l_ordinal.append([i, keywords_dict[i]])
    sql_l_simplified = [i for i in sql_l_ordinal if i[0].lower() not in arbitrary_words]

    return sql_l_simplified


def sql_ordinal(num):
    """Serves to return the ordinal numbers
    :param num:
    integer number
    :returns:
    string with the ordinal number
    """
    suff = {1: "st", 2: "nd", 3: "rd"}
    # I'm checking for 10-20 because those are the digits that
    # don't follow the normal counting scheme.
    if 10 <= num % 100 <= 20:
        suffix = "th"
    else:
        # the second parameter is a default.
        suffix = suff.get(num % 10, "th")
    return str(num) + suffix


def sql_find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start + len(needle))
        n -= 1
    return start


def sql_get_nearby_text(s, word, n):
    last_n = s.rfind("\n", 0, n - 1)
    nw = n + len(word)
    next_n = s.find("\n", nw)
    return "{}<strong>{}</strong>{}".format(
        s[last_n if last_n > 1 else s.rfind(" ", 0, n - 10) : n],
        word,
        s[nw : next_n if next_n < nw + 30 else s.find(" ", nw + 10)],
    )


def sql_get_select_into_name(st):
    """Serves to correctly identify the name of the created table for SELECT INTO statements
    :param st:
    SQL statement of SELECT INTO type
    :return:
    string with the name
    """

    next_token = False
    for token in st.tokens:
        ts = str(token).upper()
        if ts == "INTO":
            next_token = True
        elif not next_token or token.ttype in sqlparse_whitespace_t:
            pass
        else:
            tsf = ts.find("(")
            if tsf == -1:
                return ts.lower()
            else:
                return ts.lower()[:tsf]
    return None


def sql_get_alter_table_name(st):
    """Serves to correctly identify the name of the created table for ALTER TABLE statements
    :param st:
    SQL statement of ALTER TABLE type
    :return:
    string with the name
    """

    next_token = False
    for token in st.tokens:
        ts = str(token).upper()
        if ts == "TABLE":
            next_token = True
        elif not next_token or token.ttype in sqlparse_whitespace_t:
            pass
        else:
            return ts.lower()
    return None


###################################
# PRE-DEFINED POSTGRES STATEMENTS #
###################################


def select_all_check_statement(tbl):
    return "SELECT * FROM %s" % tbl


def table_created_check_statement(tbl):
    return (
        """
    SELECT
    1
    FROM pg_tables
    WHERE schemaname = current_user
    AND tablename = '%s';
    """
        % tbl
    )


def col_parameters_check_statement(tbl):
    tcc_str = ", ".join(list(table_columns_check.keys()))
    return """
    SELECT
    {}
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE table_name = '{}' AND table_schema = current_user
    """.format(
        tcc_str,
        tbl,
    )


def constraints_check_statement(tbl):
    return (
        """
    SELECT
    ccu.column_name,
    conexclop,
    conkey,
    consrc,
    contype
    -- We are not prepared to check FOREIGN KEYs right now unfortunately,
    -- it needs to be done separately, later.

    FROM information_schema.constraint_column_usage ccu

    LEFT JOIN information_schema.key_column_usage kcu
        ON ccu.constraint_catalog = kcu.constraint_catalog
        AND ccu.constraint_schema = kcu.constraint_schema
        AND ccu.constraint_name = kcu.constraint_name

    LEFT JOIN information_schema.table_constraints tc
        ON tc.constraint_catalog = ccu.constraint_catalog
        AND tc.constraint_schema = ccu.constraint_schema
        AND tc.constraint_name = ccu.constraint_name

    LEFT JOIN pg_constraint pgc
        ON tc.constraint_name = pgc.conname

    WHERE ccu.table_schema = current_user AND ccu.table_name = '%s';
    """
        % tbl
    )


def delete_check_statement(tbl):
    return "SELECT * FROM %s;" % tbl


def drop_table_statement(tbl):
    return "DROP TABLE IF EXISTS %s" % tbl


def drop_check_statement(tbl):
    return (
        "SELECT tablename FROM pg_tables WHERE schemaname = current_user AND tablename = '%s';"
        % tbl
    )


def sql_fcn_check_statement(fcn):
    return (
        """
    SELECT routine_definition,
           is_deterministic,
           is_null_call,
           data_type
    FROM information_schema.routines
    WHERE routine_name = '%s'
      AND specific_schema = current_user;
    """
        % fcn
    )


def sql_fcn_par_check_statement(fcn):
    return (
        """
    SELECT parameters.data_type,
           parameters.ordinal_position
    FROM information_schema.routines
    LEFT JOIN information_schema.parameters
           ON routines.specific_name = parameters.specific_name
    WHERE routines.routine_name = '%s'
      AND routines.specific_schema = current_user
    ORDER BY parameters.ordinal_position;
    """
        % fcn
    )


def sql_check_type_statement(type):
    return (
        """
    SELECT attname,
           attnum,
           typdefault,
           typname,
           typnotnull
    FROM pg_attribute
    LEFT JOIN pg_type
           ON pg_attribute.atttypid = pg_type.oid
    LEFT JOIN pg_namespace
           ON pg_namespace.oid = pg_type.typnamespace
    LEFT JOIN pg_class
           ON pg_attribute.attrelid = pg_class.oid
    LEFT JOIN pg_namespace n
           ON pg_class.relnamespace = n.oid
    WHERE attrelid IN (SELECT typrelid FROM pg_type WHERE typname = '%s')
      AND n.nspname = current_user
    ORDER BY attnum;
    """
        % type
    )


###########
# GRADERS #
###########


def sql_column_presence_analyzer(sol_cols, student_cols):
    """Check whether all columns are present in the result
    :param sol_cols:
    solution columns
    :param student_cols:
    student columns
    :return:
    list - empty list or list of errors
    """

    # Correct columns
    cols_correct = c(sol_cols) & c(student_cols)
    # Columns missing in the student result
    cols_missing = c(sol_cols) - c(student_cols)
    # Excess columns in the student result
    cols_excess = c(student_cols) - c(sol_cols)

    cols_text = []
    if cols_missing or cols_excess:
        if cols_correct:
            pl = len(cols_correct) > 1
            cols_correct_text = ", ".join(str(c) for c in cols_correct)
            cols_text.append(
                [
                    True,
                    "Your result correctly contains the following column%s: <code>%s</code>. "
                    % (("s" if pl else ""), cols_correct_text),
                ]
            )

        if cols_missing:
            pl = len(cols_missing) > 1
            cols_missing_text = ", ".join(str(c) for c in cols_missing)
            cols_text.append(
                [
                    False,
                    "Your result is missing the following column%s: <code>%s</code>. "
                    % (("s" if pl else ""), cols_missing_text),
                ]
            )

        if cols_excess:
            pl = len(cols_excess) > 1
            cols_excess_text = ", ".join(str(c) for c in cols_excess)
            cols_text.append(
                [
                    False,
                    "Your result contains %s not expected: <code>%s</code>. "
                    % (
                        ("these columns which are" if pl else "this column which is"),
                        cols_excess_text,
                    ),
                ]
            )

    return cols_text


def sql_column_order_analyzer(sol_cols, student_cols):
    """Check ordering of all columns
    :param sol_cols:
    solution columns
    :param student_cols:
    student columns
    :return:
    list - empty list or list of errors
    """
    cols_unordered = [j for i, j in zip(sol_cols, student_cols) if i != j]
    if cols_unordered:
        cols_unordered_text = ", ".join(str(c) for c in cols_unordered)
        return [
            [
                False,
                "These columns are not ordered correctly: <code>%s</code>"
                % cols_unordered_text,
            ]
        ]

    return []


def sql_row_analyzer(sol_rows, student_rows, sol_cols, ordering):
    """Serves to grade rows
    :param sol_rows:
    solution rows
    :param student_rows:
    student rows
    :param sol_cols:
    solution column names
    :param ordering:
    should we match the order
    :return:
    list - Errors are returned or False if no problem is found
    """

    # We use Python collections to very effectively do set operations with rows.
    # First, we update rows to hashable objects (tuple), then create collections.
    sol_rows_c = c(list(map(tuple, sol_rows)))
    student_rows_c = c(list(map(tuple, student_rows)))

    # Correct rows
    rows_correct = sol_rows_c & student_rows_c
    # Rows missing in the student result
    rows_missing = sol_rows_c - student_rows_c
    # Excess rows in the student result
    rows_excess = student_rows_c - sol_rows_c

    rows_text = []
    if rows_missing or rows_excess:
        if rows_correct:
            pl = len(rows_correct) > 1
            rows_correct_text = str(len(rows_correct))
            rows_text.append(
                [
                    True,
                    "{} {} correct. ".format(
                        rows_correct_text, ("rows are" if pl else "row is")
                    ),
                ]
            )

        # If the same number of rows is missing and not expected this number of rows is "incorrect"
        if len(rows_missing) == len(rows_excess) > 0:
            pl = len(rows_missing) > 1
            rows_missing_text = str(len(rows_missing))
            rows_text.append(
                [
                    False,
                    "%s %s not correct. "
                    % (rows_missing_text, ("rows are" if pl else "row is")),
                ]
            )

        else:
            if rows_missing:
                pl = len(rows_missing) > 1
                rows_missing_text = str(len(rows_missing))
                rows_text.append(
                    [
                        False,
                        "%s %s missing. "
                        % (rows_missing_text, ("rows are" if pl else "row is")),
                    ]
                )

            if rows_excess:
                pl = len(rows_excess) > 1
                rows_excess_text = str(len(rows_excess))
                rows_text.append(
                    [
                        False,
                        "%s %s not expected. "
                        % (rows_excess_text, ("rows are" if pl else "row is")),
                    ]
                )

    rows_set_problem = False
    if rows_text:
        rows_set_problem = True

    # Should there be any differences in collections we know about it already.
    # We still have no information about ordering.
    # We do not have to comply to any specific ordering unless ordering == True
    if not rows_set_problem and not ordering:
        return False

    if not rows_set_problem and ordering:
        # We need to check ordering
        rows_unordered = [j for i, j in zip(sol_rows, student_rows) if i != j]
        if rows_unordered:
            num_row_unordered = len(rows_unordered)
            if num_row_unordered > 3:
                return [
                    [False, "%s rows are not ordered correctly. " % (str(num_row_unordered))]
                ]
            else:
                rows_unordered_text = "\n".join(str(c) for c in rows_unordered)
                return [
                    [
                        False,
                        "These rows are not ordered correctly: <pre>%s</pre>"
                        % (rows_unordered_text),
                    ]
                ]
        else:
            return False

    # The message currently in the rows_text is adjusted if only one row is to be returned
    if rows_set_problem and len(sol_rows) == 1:
        if len(student_rows) > 1:
            rows_text = [
                [
                    False,
                    "Only one row is expected. The result has %s rows. "
                    % (str(len(student_rows))),
                ]
            ]
        elif len(student_rows) == 1 and len(sol_rows) == 1:
            # Student has only one row, but the result is different.
            student_row = student_rows[0]
            sol_row = sol_rows[0]
            row_differences = [i != j for i, j in zip(sol_row, student_row)]
            row_different_vals = [i for i, j in zip(student_row, row_differences) if j]
            cols_different = [i for i, j in zip(sol_cols, row_differences) if j]
            pl = len(cols_different) > 1
            rows_text = [
                [
                    False,
                    "%s <code>%s</code> in the column%s <code>%s</code> %s incorrect. "
                    % (
                        ("Values" if pl else "The value"),
                        "(" + ", ".join(str(c) for c in row_different_vals) + ")",
                        ("s" if pl else ""),
                        ", ".join(str(c) for c in cols_different),
                        ("are" if pl else "is"),
                    ),
                ]
            ]

    return rows_text


def sql_code_analyzer(sol_code, student_code, unimportant=None, current_user=None):
    """Serves to grade the SQL code
    :param sol_code:
    SQL solution code, usually the one in the solution cell
    :param student_code:
    SQL student code
    :return:
    list - Errors are returned or False if no problem is found
    """

    # We need both original and sanitized codes.
    sol_code_orig = str(sol_code)
    student_code_orig = str(student_code)
    sol_code = sql_code_sanitizer(sol_code_orig)
    student_code = sql_code_sanitizer(student_code_orig)

    delete_unimportant = lambda l: [x for x in l if x.upper() not in unimportant]
    if unimportant:
        unimportant = [x.upper() for x in unimportant]
        sol_code = delete_unimportant(sol_code)
        student_code = delete_unimportant(student_code)

    code_upper = lambda code: [i.upper() for i in code]
    code_upper_sol_code = code_upper(sol_code)

    if current_user:
        code_upper_sol_code = [
            i if i != "CURRENT_USER" else current_user.upper() for i in code_upper_sol_code
        ]

    sol_code_c = c(code_upper_sol_code)
    student_code_c = c(code_upper(student_code))

    # We now focus on SQL keywords only, not checking the ordering
    words_missing_all = sol_code_c - student_code_c
    words_missing = words_missing_all & c(sql_reserved)
    words_missing_sorted = sorted(words_missing)

    words_excess_all = student_code_c - sol_code_c
    words_excess = words_excess_all & c(sql_reserved)
    words_excess_sorted = sorted(words_excess)

    words_text = []
    if words_missing or words_excess:
        if words_missing:
            pl = len(words_missing) > 1
            missing_text = ", ".join(str(c) for c in words_missing)
            words_text.append(
                [
                    False,
                    "Your SQL code is missing %s: <code>%s</code>. "
                    % (("these keywords" if pl else "this keyword"), missing_text),
                ]
            )
        if words_excess:
            pl = len(words_excess) > 1
            excess_text = ", ".join(str(c) for c in words_excess)
            words_text.append(
                [
                    False,
                    "%s not expected: <code>%s</code>. "
                    % (("These keywords are" if pl else "This keyword is"), excess_text),
                ]
            )

    if words_text:
        return words_text

    # Now there are just two remaining possibilities. Either
    # the SQL command structure (ORDERING of SQL keywords) is not
    # correct or there are wrong values. We use the sql_code_simplifier()
    # function to get which keyword (with order of that keyword) has a problem
    sol_code_simplified = sql_code_simplifier(sol_code)
    student_code_simplified = sql_code_simplifier(student_code)

    # First, check the ordering of SQL keywords (this will almost never
    # be a problem unless we do multiple joins or very large SQL statements)
    keys_sol_ordered = [i for i in sol_code_simplified if i[0].upper() in sql_reserved]
    keys_student_ordered = [
        i for i in student_code_simplified if i[0].upper() in sql_reserved
    ]
    keys_student_unordered_words = [
        j
        for i, j in zip(keys_sol_ordered, keys_student_ordered)
        if i[0].lower() != j[0].lower()
    ]
    if keys_student_unordered_words:
        sco = student_code_orig
        word = keys_student_unordered_words[0][0]
        num = keys_student_unordered_words[0][1]
        needle = sql_find_nth(student_code_orig, word, num)
        return [
            [
                False,
                "Keywords around %s<code>%s</code>: <pre>%s</pre> are not in the correct order. "
                % (
                    sql_ordinal(num) + " " if num > 1 else "",
                    word,
                    sql_get_nearby_text(sco, word, needle),
                ),
            ]
        ]

    # Now we are going to check all the remaining things but aliases.
    values_student_problems = [
        j
        for i, j in zip(sol_code_simplified, student_code_simplified)
        if i[0].lower() != j[0].lower()
    ]
    if values_student_problems:
        sco = student_code_orig
        word = values_student_problems[0][0]
        num = values_student_problems[0][1]
        needle = sql_find_nth(student_code_orig, word, num)
        return [
            [
                False,
                "Check the %svalue <code>%s</code> near: <pre>%s</pre>"
                % (
                    sql_ordinal(num) + " " if num > 1 else "",
                    word,
                    sql_get_nearby_text(sco, word, needle),
                ),
            ]
        ]

    # Currently there is nothing to check regarding aliases unless we decide to be restrictive about them
    return []


def sql_select_grader(sol_code, student_code, sol_res, student_res, current_user=None):
    """Serves to grade SELECT command and the resulting table
    :param sol_code:
    SQL solution code, usually the one in the solution cell
    :param student_code:
    SQL student code
    :param sol_res:
    usually run_sql(sol_code)
    :param student_res:
    usually get_user_result()
    :return:
    list - Errors are returned or False if no problem is found
    """

    text_our_mistake = "There is a problem with testing your solution. Please <a href='https://nclab.com/contact-us/' target='_blank'>contact us</a> and include the level number. "
    text_empty = "Your code is not producing any results. Please check it and try again. "
    text_select = "Please check the instructions to see which columns are required in the <code>SELECT</code> statement. "
    text_unord = "Please check your <code>'ORDER BY'</code> criteria. "

    #################
    # Empty results #
    #################
    if not sol_res or not sol_res["columns"]:
        return [[False, text_our_mistake]]
    if not student_res or not student_res["columns"]:
        return [[False, text_empty]]

    sol_cols = sol_res["columns"]
    student_cols = student_res["columns"]
    sol_rows = sol_res["rows"]
    student_rows = student_res["rows"]

    #############################
    # ELLIPSIS or empty columns #
    #############################
    # Test if the student's code contains '...' (same as initial code):
    if "..." in student_code:
        return [
            [
                False,
                "Your code contains the ellipsis (<code>...</code>), which should have been replaced with your answer. ",
            ]
        ]
    # There is the string "?column?" if an empty column (via an empty string) was selected (e.g. SELECT '' FROM ...)
    # if '?column?' in student_cols:
    #    return [[False, text_select]]

    ######################
    # Sanitize SQL codes #
    ######################
    # We need both original and sanitized codes.
    sol_code_orig = str(sol_code)
    sol_code = sql_code_sanitizer(sol_code_orig)
    student_code_orig = str(student_code)
    student_code = sql_code_sanitizer(student_code_orig)

    #################
    # Grade COLUMNS #
    #################
    # We always grade columns first. Only correctly set columns can assure the respective rows are the same.
    # First, we check whether columns are present in the result. Then we check their order.
    # We do this in this order to provide the best possible grading messages for complex or large tables.
    cols_text = sql_column_presence_analyzer(sol_cols, student_cols)

    if cols_text:
        # Check whether there is any chance that unprocessed aggregate functions are used.
        # By unprocessed we mean directly used, without AS keyword, e.g.:
        # SELECT MAX(population) FROM ...
        # User needs a better message in this particular case, cols_text is not enough
        sol_cols_aggregate = c([x.upper() for x in sol_cols]) & c(sql_aggregate)
        if not sol_cols_aggregate:
            # No aggregate functions or user is using them actively (with AS keyword)
            return cols_text

        else:
            # Let's check properly all aggregate functions in SELECT statement
            cols_text_agg = ""
            sol_code_upper = [x.upper() for x in sol_code]
            sol_code_agg = c(sol_code_upper[: sol_code_upper.index("FROM")]) & c(
                sql_aggregate
            )
            student_code_upper = [x.upper() for x in student_code]
            student_code_agg = c(student_code_upper[: student_code_upper.index("FROM")]) & c(
                sql_aggregate
            )
            agg_missing = sol_code_agg - student_code_agg
            agg_excess = student_code_agg - sol_code_agg
            if agg_missing:
                pl = len(agg_missing) > 1
                agg_missing_text = ", ".join(str(c) for c in agg_missing)
                cols_text_agg += (
                    "<code>%s</code> %s is missing in <code>SELECT</code> statement. "
                    % (agg_missing_text, ("functions" if pl else "function"))
                )

            if agg_excess:
                pl = len(agg_excess) > 1
                agg_excess_text = ", ".join(str(c) for c in agg_excess)
                cols_text_agg += (
                    "<code>%s</code> %s should not be present in <code>SELECT</code> statement. "
                    % (agg_excess_text, ("functions" if pl else "function"))
                )

            if cols_text_agg:
                return cols_text + [[False, cols_text_agg]]
            else:
                return cols_text

    # Check the order of columns
    cols_text = sql_column_order_analyzer(sol_cols, student_cols)
    if cols_text:
        return cols_text

    ##############
    # Grade ROWS #
    ##############
    # We are now sure we have correct columns in the result.
    ordering = "ORDER BY" in sol_code
    validator_rows = sql_row_analyzer(sol_rows, student_rows, sol_cols, ordering)
    if not validator_rows:
        return []

    ##################
    # Grade SQL code #
    ##################
    validator_code = sql_code_analyzer(
        sol_code_orig, student_code_orig, current_user=current_user
    )

    return validator_rows + validator_code


def sql_create_or_alter_table_grader(test_tbl_cols, student_tbl_cols, table_cols_check=None):
    """Serves to grade CREATE TABLE or ALTER TABLE commands
    :param test_tbl_cols:
    columns of the test table
    :param student_tbl_cols:
    columns of the table created by a student
    :param table_cols_check:
    dict of column parameters to check, default dict is used if not provided
    :return:
    list - Errors are returned or False if no problem is found
    """

    test_tbl_colnames = [i[0] for i in test_tbl_cols]
    student_tbl_colnames = [i[0] for i in student_tbl_cols]
    if not table_cols_check:
        table_cols_check = table_columns_check

    # Check whether the table exists
    if not student_tbl_colnames:
        return [[False, "Table was not created. "]]

    cols_text = sql_column_presence_analyzer(test_tbl_colnames, student_tbl_colnames)
    if cols_text:
        return cols_text

    # Now we know that correct columns are present in the created table
    # Let's check the parameters of the table provided in the rows.
    # Do not take into account the ordering now (first we will order it).
    ind_name = list(table_cols_check.keys()).index("column_name")
    sorted_test_tbl_cols = sorted(test_tbl_cols, key=operator.itemgetter(ind_name))
    sorted_student_tbl_cols = sorted(student_tbl_cols, key=operator.itemgetter(ind_name))
    cols_different = [
        [list(table_cols_check.keys()), i, j]
        for i, j in zip(sorted_test_tbl_cols, sorted_student_tbl_cols)
        if i != j
    ]

    cols_text = []
    for i in cols_different:
        col_name = i[1][ind_name]
        column_text = "Column <code>%s</code> is not correctly set. " % col_name

        groups = list(zip(i[0], i[1], i[2]))
        col_differences = [group for group in groups if group[1] != group[2]]

        pl = len(col_differences) > 1
        param_text = ", ".join(str(table_cols_check[c[0]]) for c in col_differences)
        cols_text += [
            [
                False,
                column_text
                + " There %s column %s: <code>%s</code>. "
                % (
                    (
                        "are problems with following"
                        if pl
                        else "is a problem with the following"
                    ),
                    ("parameters" if pl else "parameter"),
                    param_text,
                ),
            ]
        ]

    if cols_text:
        return cols_text

    # Check the order of columns
    cols_text = sql_column_order_analyzer(test_tbl_colnames, student_tbl_colnames)

    return cols_text


def sql_table_constraints_grader(constraints_check_sol, constraints_check_student):
    """Serves to check and grade constraints on a table and columns
    :param constraints_check_sol:
    result of constraints check SQL solution code
    :param constraints_check_student:
    result of constraints check SQL student code
    :return:
    string - Error is returned or False if no problem is found
    """
    # Construct the set of constraints
    sol_cons_set = set(map(tuple, constraints_check_sol["rows"]))
    student_cons_set = set(map(tuple, constraints_check_student["rows"]))

    # Correct
    cons_correct = sol_cons_set.intersection(student_cons_set)
    # Missing
    cons_missing = sol_cons_set.difference(student_cons_set)
    # Excess
    cons_excess = student_cons_set.difference(sol_cons_set)

    table_cons_check = {
        "c": "check constraint",
        "f": "foreign key constraint",
        "p": "primary key constraint",
        "u": "unique constraint",
        "t": "constraint trigger",
        "x": "exclusion constraint",
    }
    cols = constraints_check_sol["columns"]
    column_name = cols.index("column_name")
    consrc = cols.index("consrc")
    contype = cols.index("contype")

    cons_text = []
    if cons_missing or cons_excess:
        if cons_missing:
            cons_missing_text = " ".join(
                "Column <code>%s</code> is missing a <strong>%s</strong>%s. "
                % (
                    str(c[column_name]),
                    str(table_cons_check[c[contype]]),
                    ""
                    if c[contype] != "c"
                    else " (details: <code>%s</code>)" % str(c[consrc]),
                )
                for c in cons_missing
            )
            cons_text += [[False, cons_missing_text]]

        if cons_excess:
            cons_excess_text = " ".join(
                "In column <code>%s</code> a <strong>%s</strong> is not expected%s. "
                % (
                    str(c[column_name]),
                    str(table_cons_check[c[contype]]),
                    ""
                    if c[contype] != "c"
                    else " (details: <code>%s</code>)" % str(c[consrc]),
                )
                for c in cons_excess
            )
            cons_text += [[False, cons_excess_text]]
        return cons_text

    return []


def sql_insert_grader(
    sol_res,
    student_res,
    colums_not_graded=[],
    columns_not_null=[],
    columns_null=[],
    sol_code=False,
    student_code=False,
):
    """Serves to grade SELECT command and the resulting table
    :param sol_res:
    usually run_sql(sol_code)
    :param student_res:
    usually run_sql(student_code)
    :param columns_not_graded:
    list of names of columns which will be not graded
    :param columns_not_null:
    list of names of columns which must not be NULL
    :param columns_null:
    list of names of columns which have to be NULL (examples for students need this sometimes)
    :param sol_code:
    (optional) SQL code of the solution
    :param student_code:
    (optional) SQL code of the student
    :return:
    string - Error is returned or False if no problem is found
    """

    sol_cols = sol_res["columns"]
    student_cols = student_res["columns"]
    sol_rows = sol_res["rows"]
    student_rows = student_res["rows"]

    ###########################################
    # Check special NULL and NOT NULL columns #
    ###########################################
    # We can now use sets as order is not important.
    # Check indices of columns_not_null and columns_null
    not_null_cols_indices = [sol_cols.index(i) for i in columns_not_null if i in sol_cols]
    null_cols_indices = [sol_cols.index(i) for i in columns_null if i in sol_cols]

    # Check excess rows only for now (only checking special columns)
    sol_rows_set = c(list(map(tuple, sol_rows)))
    student_rows_set = c(list(map(tuple, student_rows)))
    rows_excess = list(student_rows_set - sol_rows_set)

    incorrect_null_rows = [
        [i for ind, j in enumerate(i) if ind in not_null_cols_indices and j == "NULL"]
        for i in rows_excess
    ]
    incorrect_null_rows_present = not isListEmpty(incorrect_null_rows)
    if incorrect_null_rows_present:
        return "There is a NULL value where it should not be. Try to INSERT correct values again. "

    incorrect_not_null_rows = [
        [i for ind, j in enumerate(i) if ind in null_cols_indices and j != "NULL"]
        for i in rows_excess
    ]
    incorrect_not_null_rows_present = not isListEmpty(incorrect_not_null_rows)
    if incorrect_not_null_rows_present:
        return "There is a non-trivial value where NULL should be. Try to INSERT correct values again. "

    ###############################
    # Removing unrelevant columns #
    ###############################
    not_relevant_cols_indices = [
        sol_cols.index(i) for i in colums_not_graded if i in sol_cols
    ]
    rem_unrel = lambda a: [
        [j for ind, j in enumerate(i) if ind not in not_relevant_cols_indices] for i in a
    ]
    sol_rows = rem_unrel(sol_rows)
    student_rows = rem_unrel(student_rows)
    cols = [j for ind, j in enumerate(sol_cols) if ind not in not_relevant_cols_indices]

    ##############
    # Grade ROWS #
    ##############
    # We are now sure we have only relevant columns in the result.
    ordering = False
    validator_rows = sql_row_analyzer(sol_rows, student_rows, sol_cols, ordering)
    if not validator_rows:
        return []

    ##################
    # Grade SQL code #
    ##################
    validator_code = []
    if sol_code and student_code:
        validator_code = sql_code_analyzer(sol_code, student_code)

    return validator_rows + validator_code


def sql_delete_grader(sol_code, student_code, sol_res, student_res):
    """Serves to grade DELETE command and the resulting table
    :param sol_code:
    SQL solution code, usually the one in the solution cell
    :param student_code:
    SQL student code
    :param sol_res:
    usually run_sql(sol_code)
    :param student_res:
    usually get_user_result()
    :return:
    list - Errors are returned or False if no problem is found
    """

    sol_cols = sol_res["columns"]
    student_cols = student_res["columns"]
    sol_rows = sol_res["rows"]
    student_rows = student_res["rows"]

    ######################
    # Sanitize SQL codes #
    ######################
    # We need both original and sanitized codes.
    sol_code_orig = str(sol_code)
    sol_code = sql_code_sanitizer(sol_code_orig)
    student_code_orig = str(student_code)
    student_code = sql_code_sanitizer(student_code_orig)

    ##############
    # Grade ROWS #
    ##############
    ordering = "ORDER BY" in sol_code
    validator_rows = sql_row_analyzer(sol_rows, student_rows, sol_cols, ordering)
    if not validator_rows:
        return []

    ##################
    # Grade SQL code #
    ##################
    validator_code = sql_code_analyzer(sol_code_orig, student_code_orig)

    return validator_rows + validator_code


def sql_drop_table_grader(what_to_drop, tables):
    """Serves to grade DROP command
    :param what_to_drop:
    What should be dropped
    :param tables:
    list of all tables, table name is the first column
    :return:
    string - Error is returned or False if no problem is found
    """

    flattened = [i[0] for i in tables]

    if not what_to_drop in flattened:
        return False
    else:
        return "The table <code>%s</code> was not dropped. Please try again. " % what_to_drop


def sql_function_grader(sol_row, student_row, cols):
    """Serves to grade function setup (no parameter grading here)
    :param sol_row:
    technical parameters of the solution function
    :param student_code:
    technical parameters of the student function
    :param cols:
    meaning of positions in the list
    :return:
    string - Error is returned or False if no problem is found
    """

    cols_legend = {
        "is_deterministic": "immutability",
        "is_null_call": "automatic returning <code>NULL</code>",
        "data_type": "data type of the function",
    }

    # We were removing SQL source code of the function, this is graded by other grader
    src_ind = cols.index("routine_definition")
    src_remove = lambda x: x.pop(src_ind)
    src_remove(sol_row)
    src_remove(student_row)
    src_remove(cols)

    problems = [
        [j, k] for i, j, k in itertools.zip_longest(sol_row, student_row, cols) if i != j
    ]
    if problems:
        problem = problems[0]
        value = problem[0]
        legend = cols_legend[problem[1]]

        return "Check the value of {} parameter (<code>{}</code>) of the function. ".format(
            legend,
            value,
        )

    return False


def sql_function_parameters_grader(sol_fcn_pars, student_fcn_pars, sol_fcn):
    """Serves to grade function parameters
    :param sol_fcn_pars:
    parameters of the solution function
    :param student_fcn_pars:
    parameters of the student function
    :return:
    string - Error is returned or False if no problem is found
    """

    problems = [j for i, j in itertools.zip_longest(sol_fcn_pars, student_fcn_pars) if i != j]

    if problems:
        word = problems[0][0] if problems[0] != None else False
        num = int(problems[0][1]) if problems[0] != None else 0
        return (
            "Check the %sparameter (<code>%s</code>) of function <code>%s</code>. "
            % (sql_ordinal(num) + " " if num > 0 else "", word, sol_fcn)
            if word
            else "Check for missing parameters of the function <code>%s</code>. " % sol_fcn
        )

    return False


def sql_function_tests_grader(results, sol_fcn_src, student_fcn_src, sol_fcn):
    """Serves to grade function parameters
    :param results:
    results of test calls
    :param sol_fcn_src:
    solution function source code
    :param student_fcn_src:
    student function source code
    :param sol_fcn:
    name of the function
    :return:
    list - Errors are returned or False if no problem is found
    """

    problems = [[i, j, k, l] for i, j, k, l in results if j != k]
    problem = problems[0] if problems else False

    if problem:
        problem_message = (
            "Testing function <code>%s</code> with random values: <code>%s</code>. "
            % (sol_fcn, str(problem[0] if problem[0] else ""))
        )
        messages = []
        validator = sql_row_analyzer(problem[2], problem[1], problem[3], True)
        if validator:
            validator[0][1] = problem_message + validator[0][1]
            messages += validator
        validator = sql_code_analyzer(sol_fcn_src, student_fcn_src)
        if validator:
            messages += validator

        return messages

    return False


def sql_type_grader(sol_type_pars, student_type_pars, cols, sol_type):
    """Serves to grade type
    :param sol_type_pars:
    parameters of the solution type
    :param student_type_pars:
    parameters of the student type
    :param cols:
    meaning of positions in a parameter list
    :param sol_type:
    name of the type
    :return:
    string - Error is returned or False if no problem is found
    """

    problems = [
        [j, k]
        for i, j, k in itertools.zip_longest(sol_type_pars, student_type_pars, cols)
        if i != j
    ]

    if problems:
        word = problems[0][0][0] if problems[0] != None and problems[0][0] != None else False
        num = int(problems[0][0][1]) if (problems[0][0] != None) else 0
        return (
            "Check the %sparameter (<code>%s</code>) of type <code>%s</code>. "
            % (sql_ordinal(num) + " " if num > 0 else "", word, sol_type)
            if word
            else "Check for missing parameters of the type <code>%s</code>. " % sol_type
        )

    return False


#################
# GLOBAL GRADER #
#################


def sql_sttype_extraction(statement):
    """Extracts the statement types
    :param code:
    list of statements
    :return:
    list - list of statements
    """

    st_tokens = []
    for token in statement.tokens:
        ts = str(token).upper()
        if len(st_tokens) == 1 and st_tokens[0] == "SELECT":
            if ts == "INTO":
                st_tokens.append(ts)
                break
            elif ts == "FROM":
                break
            else:
                pass
        elif ts == "IF":  # Do not take into account IF EXISTS part of some statements
            break
        elif token.ttype in sqlparse_keyword_t:
            st_tokens.append(ts)
        elif token.ttype in sqlparse_whitespace_t:
            pass
        else:
            break

    return " ".join(st_tokens)


def sql_identify_optional(sts, opt):
    """Serves identify an optional statement (only one allowed)
    :param sol_code:
    SQL solution code, list of statements
    :param opt:
    The parameter which defines the optional statement (int or str)
    :return:
    int - (-1) if not found, other value if found
    """

    i = -1
    if isinstance(opt, str):
        i = 0
        for st in sts:
            if opt in st:
                break
            else:
                i += 1
    elif opt is int:
        i = opt
    if 0 <= i < len(sts):
        return i
    else:
        return -1


def sql_global_grader_opt(sol_code, student_code, opt=None):
    """Serves to grade the sutdent code regarding number and types of statements (sts),
    should be run first, before other graders
    :param sol_code:
    SQL solution code, usually the one in the solution cell
    :param student_code:
    SQL student code
    :param opt:
    Optional parameter with int or str which points to a optional statement
    :return:
    (string, opt) - Error is returned or False if no problem is found, opt is
    the identified optional parameter, opt is returned only if input opt is not None,
    otherwise only one value (string) is returned
    """

    # Test whether a student wrote any code
    if len(student_code) == 0:
        return "Please write a SQL command before submitting. "

    get_sts = lambda i: [sql_sttype_extraction(s) for s in i]
    sol_sts = get_sts(sol_code)
    student_sts = get_sts(student_code)

    # Function opt is a parameter which can make a statement optional
    if opt:
        i = sql_identify_optional(sol_sts, opt)
        if i >= 0 and sol_sts[i] != student_sts[i] and len(sol_sts) > len(student_sts):
            sol_sts.pop(i)
        else:
            i = -1

    sol_c = c(sol_sts)
    student_c = c(student_sts)

    # We now focus on SQL keysts only, not checking the ordering
    sts_missing = sol_c - student_c
    sts_excess = student_c - sol_c

    sts_text = ""
    if sts_missing or sts_excess:
        if sts_missing:
            pl = len(sts_missing) > 1
            missing_text = ", ".join(
                "{}{}".format(key, " (%i&times;)" % value if value > 1 else "")
                for (key, value) in list(sts_missing.items())
            )
            sts_text += "Your SQL code is missing {}: <code>{}</code>. ".format(
                ("these statements" if pl else "this statement"),
                missing_text,
            )
        if sts_excess:
            # We need to handle the excess of INSERT INTO statements separately
            sts_excess_list = list(sts_excess)
            if len(sts_excess_list) == 1 and "INSERT INTO" in sts_excess_list:
                # DEV-2727: Specific change of the error message if multiple INSERT INFO are used
                sts_text += """There are too many <code>INSERT INTO</code> statements. Please <a
                               href='https://www.postgresql.org/docs/current/sql-insert.html#id-1.9.3.152.9'
                               target='_blank'>merge them</a> into one before submitting."""
            else:
                pl = len(sts_excess) > 1
                excess_text = ", ".join(
                    "{}{}".format(key, " (%i&times;)" % value if value > 1 else "")
                    for (key, value) in list(sts_excess.items())
                )
                sts_text += "{} not expected: <code>{}</code>. ".format(
                    ("These statements are" if pl else "This statement is"),
                    excess_text,
                )

    if sts_text and opt:
        return (sts_text, i)
    elif sts_text and not opt:
        return sts_text

    unordered_sts = [j for i, j in zip(sol_sts, student_sts) if i != j]
    if unordered_sts:
        return (
            "Statements near <code>'%s'</code> are not in the correct order. "
            % (unordered_sts[0]),
            i,
        )

    if opt:
        return (sts_text, i)
    else:
        return sts_text


#####################
# ABANDONED GRADERS # - TODO: to be deleted in the future after courses are updated with new ones
#####################


def sql_create_table_grader(
    sol_code, student_code, test_tbl_cols, student_tbl_cols, table_cols_check=None
):
    """Serves to grade CREATE TABLE command
    :param sol_code:
    SQL solution code, usually the one in the solution cell
    :param student_code:
    SQL student code
    :param test_tbl_cols:
    columns of the test table
    :param student_tbl_cols:
    columns of the table created by a student
    :param table_cols_check:
    dict of column parameters to check
    :return:
    string - Error is returned or False if no problem is found
    """

    test_tbl_colnames = [i[0] for i in test_tbl_cols]
    student_tbl_colnames = [i[0] for i in student_tbl_cols]
    if not table_cols_check:
        table_cols_check = table_columns_check

    # First, the same way as for the SELECT autograder, we look on the
    # set of all columns whether some are missing or not expected
    sol_cols_c = c(test_tbl_colnames)
    student_cols_c = c(student_tbl_colnames)

    # Correct columns
    cols_correct = sol_cols_c & student_cols_c
    # Columns missing in the student result
    cols_missing = sol_cols_c - student_cols_c
    # Excess columns in the student result
    cols_excess = student_cols_c - sol_cols_c

    cols_text = ""
    if cols_missing or cols_excess:
        if cols_missing:
            pl = len(cols_missing) > 1
            cols_missing_text = ", ".join(str(c) for c in cols_missing)
            cols_text += (
                "Your result is missing the following column%s: <code>%s</code>. "
                % (("s" if pl else ""), cols_missing_text)
            )

        if cols_excess:
            pl = len(cols_excess) > 1
            cols_excess_text = ", ".join(str(c) for c in cols_excess)
            cols_text += "Your result contains {} not expected: <code>{}</code>. ".format(
                ("these columns which are" if pl else "this column which is"),
                cols_excess_text,
            )
        return cols_text

    # Now we know that correct columns are present in the created table
    # Let's check the parameters of all rows now.
    # Do not take into account the ordering now (first we will order it).
    ind_name = list(table_cols_check.keys()).index("column_name")
    sorted_test_tbl_cols = sorted(test_tbl_cols, key=operator.itemgetter(ind_name))
    sorted_student_tbl_cols = sorted(student_tbl_cols, key=operator.itemgetter(ind_name))
    cols_different = [
        [list(table_cols_check.keys()), i, j]
        for i, j in zip(sorted_test_tbl_cols, sorted_student_tbl_cols)
        if i != j
    ]

    cols_text = ""
    for i in cols_different:
        col_name = i[1][ind_name]
        cols_text = "Column <code>%s</code> is not correctly set. " % col_name

        groups = list(zip(i[0], i[1], i[2]))
        col_differences = [group for group in groups if group[1] != group[2]]

        pl = len(col_differences) > 1
        param_text = ", ".join(str(c[0]) for c in col_differences)
        cols_text += "There {} column {}: <code>{}</code>. ".format(
            ("are problems with following" if pl else "is a problem with the following"),
            ("parameters" if pl else "parameter"),
            param_text,
        )

    if cols_text:
        return cols_text

    # The order of columns is important, so that we can use INSERT ... VALUES ... later
    cols_order_diff = [i for i, j in zip(test_tbl_colnames, student_tbl_colnames) if i != j]
    if cols_order_diff:
        cols_order_text = ", ".join("<code>%s</code>" % str(c) for c in cols_order_diff)
        cols_text = "Columns %s are not ordered properly. " % cols_order_text

    return cols_text


def sql_alter_table_grader(
    sol_code, student_code, test_tbl_cols, student_tbl_cols, table_cols_check
):
    """Serves to grade CREATE TABLE command
    :param sol_code:
    SQL solution code, usually the one in the solution cell
    :param student_code:
    SQL student code
    :param test_tbl_cols:
    columns of the test table
    :param student_tbl_cols:
    columns of the table created by a student
    :param table_cols_check:
    dict of column parameters to check
    :param student_rows:
    usually get_user_result()['rows']
    :return:
    string - Error is returned or False if no problem is found
    """

    test_tbl_colnames = [i[0] for i in test_tbl_cols]
    student_tbl_colnames = [i[0] for i in student_tbl_cols]

    # First, the same way as for the SELECT autograder, we look on the
    # set of all columns whether some are missing or not expected
    sol_cols_c = c(test_tbl_colnames)
    student_cols_c = c(student_tbl_colnames)

    # Correct columns
    cols_correct = sol_cols_c & student_cols_c
    # Columns missing in the student result
    cols_missing = sol_cols_c - student_cols_c
    # Excess columns in the student result
    cols_excess = student_cols_c - sol_cols_c

    cols_text = ""
    if cols_missing or cols_excess:
        if cols_missing:
            pl = len(cols_missing) > 1
            cols_missing_text = ", ".join(str(c) for c in cols_missing)
            cols_text += (
                "Your result is missing the following column%s: <code>%s</code>. "
                % (("s" if pl else ""), cols_missing_text)
            )

        if cols_excess:
            pl = len(cols_excess) > 1
            cols_excess_text = ", ".join(str(c) for c in cols_excess)
            cols_text += "Your result contains {} not expected: <code>{}</code>. ".format(
                ("these columns which are" if pl else "this column which is"),
                cols_excess_text,
            )
        return cols_text

    # Now we know that correct columns are present in the created table
    # Let's check the parameters of all rows now.
    # Do not take into account the ordering now (first we will order it).
    ind_name = list(table_cols_check.keys()).index("column_name")
    sorted_test_tbl_cols = sorted(test_tbl_cols, key=operator.itemgetter(ind_name))
    sorted_student_tbl_cols = sorted(student_tbl_cols, key=operator.itemgetter(ind_name))
    cols_different = [
        [list(table_cols_check.keys()), i, j]
        for i, j in zip(sorted_test_tbl_cols, sorted_student_tbl_cols)
        if i != j
    ]

    cols_text = ""
    for i in cols_different:
        col_name = i[1][ind_name]
        cols_text = "Column <code>%s</code> is not correctly set. " % col_name

        groups = list(zip(i[0], i[1], i[2]))
        col_differences = [group for group in groups if group[1] != group[2]]

        pl = len(col_differences) > 1
        param_text = ", ".join(str(c[0]) for c in col_differences)
        cols_text += "There {} column {}: <code>{}</code>. ".format(
            ("are problems with following" if pl else "is a problem with the following"),
            ("parameters" if pl else "parameter"),
            param_text,
        )

    if cols_text:
        return cols_text

    # The order of columns is important, so that we can use INSERT ... VALUES ... later
    cols_order_diff = [i for i, j in zip(test_tbl_colnames, student_tbl_colnames) if i != j]
    if cols_order_diff:
        cols_order_text = ", ".join("<code>%s</code>" % str(c) for c in cols_order_diff)
        cols_text = "Columns %s are not ordered properly. " % cols_order_text

    return cols_text


def sql_constraints_grader(constraints_check_sol, constraints_check_student):
    """Serves to check and grade constraints on a table and columns
    :param constraints_check_sol:
    result of constraints check SQL solution code
    :param constraints_check_student:
    result of constraints check SQL student code
    :return:
    string - Error is returned or False if no problem is found
    """
    # Construct the set of constraints
    sol_cons_set = set(map(tuple, constraints_check_sol["rows"]))
    student_cons_set = set(map(tuple, constraints_check_student["rows"]))

    # Correct
    cons_correct = sol_cons_set.intersection(student_cons_set)
    # Missing
    cons_missing = sol_cons_set.difference(student_cons_set)
    # Excess
    cons_excess = student_cons_set.difference(sol_cons_set)

    table_cons_check = {
        "c": "check constraint",
        "f": "foreign key constraint",
        "p": "primary key constraint",
        "u": "unique constraint",
        "t": "constraint trigger",
        "x": "exclusion constraint",
    }
    cols = constraints_check_sol["columns"]
    column_name = cols.index("column_name")
    consrc = cols.index("consrc")
    contype = cols.index("contype")

    cons_text = ""
    if cons_missing or cons_excess:
        if cons_missing:
            cons_missing_text = " ".join(
                "Column <code>%s</code> is missing a <strong>%s</strong>%s. "
                % (
                    str(c[column_name]),
                    str(table_cons_check[c[contype]]),
                    ""
                    if c[contype] != "c"
                    else " (details: <code>%s</code>)" % str(c[consrc]),
                )
                for c in cons_missing
            )
            cons_text += cons_missing_text

        if cons_excess:
            cons_excess_text = " ".join(
                "In column <code>%s</code> a <strong>%s</strong> is not expected%s. "
                % (
                    str(c[column_name]),
                    str(table_cons_check[c[contype]]),
                    ""
                    if c[contype] != "c"
                    else " (details: <code>%s</code>)" % str(c[consrc]),
                )
                for c in cons_excess
            )
            cons_text += cons_excess_text
        return cons_text
    return False


def sql_global_grader(sol_code, student_code):
    """Serves to grade the student code regarding number and types of statements (sts),
    should be run first, before other graders
    :param sol_code:
    SQL solution code, usually the one in the solution cell
    :param student_code:
    SQL student code
    :return:
    string - Error is returned or False if no problem is found
    """

    def sttype_extraction(statement):
        st_tokens = []
        for token in statement.tokens:
            ts = str(token).upper()
            if len(st_tokens) == 1 and st_tokens[0] == "SELECT":
                if ts == "INTO":
                    st_tokens.append(ts)
                    break
                elif ts == "FROM":
                    break
                else:
                    pass
            elif token.ttype in sqlparse_keyword_t:
                st_tokens.append(ts)
            elif token.ttype in sqlparse_whitespace_t:
                pass
            else:
                break
        return " ".join(st_tokens)

    get_sts = lambda i: [sttype_extraction(s) for s in i]
    sol_sts = get_sts(sol_code)
    student_sts = get_sts(student_code)

    sol_c = c(sol_sts)
    student_c = c(student_sts)

    # We now focus on SQL keysts only, not checking the ordering
    sts_missing = sol_c - student_c
    sts_missing_sorted = sorted(sts_missing)

    sts_excess = student_c - sol_c
    sts_excess_sorted = sorted(sts_excess)

    sts_text = ""
    if sts_missing or sts_excess:
        if sts_missing:
            pl = len(sts_missing) > 1
            missing_text = ", ".join(str(c) for c in sts_missing)
            sts_text += "Your SQL code is missing {}: <code>{}</code>. ".format(
                ("these statements" if pl else "this statement"),
                missing_text,
            )
        if sts_excess:
            pl = len(sts_excess) > 1
            excess_text = ", ".join(str(c) for c in sts_excess)
            sts_text += "{} not expected: <code>{}</code>. ".format(
                ("These statements are" if pl else "This statement is"),
                excess_text,
            )

    if sts_text:
        return sts_text

    unordered_sts = [j for i, j in zip(sol_sts, student_sts) if i != j]
    if unordered_sts:
        return "Statements near <code>'%s'</code> are not in the correct order. " % (
            unordered_sts[0]
        )

    return sts_text
