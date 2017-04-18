import subprocess

'''
K-Anonymity Configuration File Format:
Json file contains:
"<AttributeType>":[<Column name1>,<Column name2>]

AttributeType includes:
1. sensitive: This column will be suppressed completely
2. insensitive: Nothing will be done to this column
3. identifying: This will be anonymized by k-anonymity algorithm
4. age: Specifiy that this column is age and identifying
5. zip: Specifiy that this column is zip and identifying

If a column is not mentioned in the configuration file,
it will be seen as sensitive by the algorithm

example:
{
    "insensitive": [column name1, column name2, column name3],
    "sensitive": [column name4, column name5],
    "identifying": [column name6, column name7, column name8],
    "age": [column name9],
    "zip": [column name10],
    "k": 5
}

'''

def __subprocess_cmd(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print proc_stdout


def k_anonymity(src_path, conf_path, dest_path):
    cmd = """
    cd arx
    javac -cp libarx-3.5.1.jar:json-simple-1.1.1.jar Anonymity.java
    java -cp libarx-3.5.1.jar:json-simple-1.1.1.jar:. Anonymity {} {} {}
    rm ./*.class
    rm ./*.json
    """.format(src_path, conf_path, dest_path)
    __subprocess_cmd(cmd)

