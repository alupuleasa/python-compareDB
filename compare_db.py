import db_connect
import dumper
import json

DB1 = dict(
    user = "root",
    password = "pass4root",
    host = "localhost",
    port = 3306,
    name = "comparedb"
)

DB2 = dict(
    user = "root",
    password = "pass4root",
    host = "localhost",
    port = 3306,
    name = "comparedb2"
)

colProps = ("Field","Type","Collation","Null","Key","Default","Extra","Privileges","Comment")

class CompareDB:
    def __init__(self) -> None:
        self.DB1 =  db_connect.dbConnect(DB1)
        self.DB1.host = DB1["host"]
        self.DB1.name = DB1["name"]
        self.DB1.tables = self.getDatabaseStructure(self.DB1)
        self.DB2 =  db_connect.dbConnect(DB2)
        self.DB2.host = DB2["host"]
        self.DB2.name = DB2["name"]
        self.DB2.tables = self.getDatabaseStructure(self.DB2)
    def __str__(self) -> str:
        # return json.dumps(self.DB1.tables)
        return json.dumps(self.compareDatabases(self.DB1, self.DB2))
    def getDatabaseStructure(self, DB):
        tables = self.getTables(DB)
        dbTablesList = list()
        for table in tables:
            tableData = dict()
            tableData['tableName'] = table[0] 
            tableData['tableType'] = table[1]
            tableData['tableRows'] = self.getTableRows(DB, table[0])[0][0]
            tableData['columns'] = self.describeTable(DB, table[0])
            dbTablesList.append(tableData)

        return dbTablesList

    def compareDatabases(self, DB1Struct, DB2Struct):
        if DB1Struct.host == DB2Struct.host:
            DB1 = DB1Struct.name
            DB2 = DB2Struct.name
        else:
            DB1 = DB1Struct.host
            DB2 = DB2Struct.host

        diffsDB = list()
        for table in DB1Struct.tables:
            diffDB = dict()
            diffDB[table["tableName"]] = dict()
            ok = 0
            for table2 in DB2Struct.tables:
                if table["tableName"] == table2["tableName"]:
                    ok = 1
                    if table["tableRows"] != table2["tableRows"]:
                        diffDB[table["tableName"]]["rows"] = f'{DB1}({table["tableRows"]}) - {DB2}({table2["tableRows"]})'
                    
                    diffDB[table["tableName"]]["columns"] = dict()
                    for column in table["columns"]:
                        innerOk = 0
                        for column2 in table2["columns"]:
                            if column["Field"] == column2["Field"]:
                                innerOk = 1
                                diffDB[table["tableName"]]["columns"][column["Field"]] = dict()
                                for colProp in colProps:
                                    if column[colProp] != column2[colProp]:
                                        diffDB[table["tableName"]]["columns"][column["Field"]][colProp] = f'{DB2}({colProp} => {column[colProp]}) => {DB1}({colProp} => {column2[colProp]})'
                        if innerOk == 0:
                            diffDB[table["tableName"]]["columns"][column["Field"]] = f'Column missing on {DB2}'
            if ok == 0:
                diffDB[table["tableName"]] = f'{table["tableType"]} missing on {DB2}'
            diffsDB.append(diffDB)
        return diffsDB

    def getTableRows(self, DB, table):
        return DB.executeQuery(f'SELECT COUNT(*) as tableRows FROM {table}')
    def getTables(self, DB):
        return DB.executeQuery('SHOW FULL TABLES')
    def describeTable(self, DB, table):
        colsVal = DB.executeQuery(f'SHOW FULL COLUMNS FROM {table}')
        cols = list()
        for colVal in colsVal:
            cols.append(dict(zip(colProps, colVal)))
        return cols
