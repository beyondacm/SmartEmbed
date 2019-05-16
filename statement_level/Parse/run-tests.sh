#!/bin/bash

ANTLR_JAR="antlr4.jar"

GRAMMAR="Solidity"
START_RULE="sourceUnit"
TEST_FILE="test.sol"
ERROR_PATTERN="mismatched|extraneous"

if [ ! -e "$ANTLR_JAR" ]; then
  curl http://www.antlr.org/download/antlr-4.7-complete.jar -o "$ANTLR_JAR"
fi

mkdir -p target/

java -jar $ANTLR_JAR $GRAMMAR.g4 -o src/
javac -classpath $ANTLR_JAR src/*.java -d target/

java -classpath $ANTLR_JAR:target/ org.antlr.v4.gui.TestRig "$GRAMMAR" "$START_RULE" < "$TEST_FILE" 2>&1 |
  grep -qE "$ERROR_PATTERN" && echo "TESTS FAIL!" || echo "TESTS PASS!"

# java -classpath ./antlr4.jar:./target Tokenize 
# java -classpath ./antlr4.jar:./target Tokenize /home/zhipeng/work_space/Vulnerable_Smart_Contract/stp01_crawl/0x00f90986CDD79744409F8a3c7747064AFa4473b5/ #>& ParserOutput 

