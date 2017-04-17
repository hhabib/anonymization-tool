import subprocess

'''
K-Anonymity Configuration File Format:
Json file contains:
"<Column name>": <AttributeType>

AttributeType includes:
1. Sensitive: This column will be suppressed completely
2. Insensitive: Nothing will be done to this column
3. Identifying: This will be anonymized by k-anonymity algorithm
4. Identifying-Age: Specifiy that this column is age and identifying
5. Identifying-Zip: Specifiy that this column is zip and identifying

If a column is not mentioned in the configuration file,
it will be seen as sensitive by the algorithm

example:
{
    "Death Date": "Insensitive",
    "Manner of Death": "Identifying",
    "Age": "Identifying-Age",
    "Sex": "Identifying",
    "Race": "Identifying",
    "Case Dispo": "Identifying",
    "Incident Zip": "Identifying-Zip",
    "Decedent Zip": "Identifying-Zip",
    "Case Year": "Identifying",
}

'''

def __subprocess_cmd(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print proc_stdout


def k_anonymity(src_path, k, conf_path, dest_path):
    cmd = """
    cd arx
    javac -cp libarx-3.5.1.jar:json-simple-1.1.1.jar Anonymity.java
    java -cp libarx-3.5.1.jar:json-simple-1.1.1.jar:. Anonymity {} {} {} {}
    rm ./*.class
    rm ./*.json
    """.format(src_path, k, conf_path, dest_path)
    __subprocess_cmd(cmd)

