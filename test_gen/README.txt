This test script generator generates the random insertion data. But it does not take into account the edge cases which are not supported. So the database will throw an error for some of the generated data during insertion. For running it:

python3 test_gen.py <numberOfInsertionsPerTable>
