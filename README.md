算法与数据结构练习（Python3）
=====

作者:Chai Fei   
E-mail:cforth [at] cfxyz.com  
主要是Python写的算法与数据结构练习代码，还有《计算的本质：深入剖析程序和计算机》这本书中的演示代码。书中是Ruby语言实现的，我改写成了Python语言实现。


combinations
------------
数学中的组合、排列、枚举算法的演示代码。以及我设计的一种多进制数算术系统的实现。  
1. [集合中所有组合的生成算法](https://github.com/cforth/toys/blob/master/combinations/combinations_generater.py)  
2. [集合中所有排列的生成算法](https://github.com/cforth/toys/blob/master/combinations/permutations_generater.py)  
3. [集合中所有枚举的生成算法](https://github.com/cforth/toys/blob/master/combinations/enumerations_generater.py)  
4. [多进制数算术系统的实现](https://github.com/cforth/toys/blob/master/combinations/MultiInt.py)


sort
------------
常用的排序算法的演示代码。  
1. [选择排序算法](https://github.com/cforth/toys/blob/master/sort/selection_sort.py)  
2. [插入排序算法](https://github.com/cforth/toys/blob/master/sort/insertion_sort.py)  
3. [希尔排序算法](https://github.com/cforth/toys/blob/master/sort/shell_sort.py)  
4. [合并排序算法](https://github.com/cforth/toys/blob/master/sort/merge_sort.py)  
5. [堆排序算法](https://github.com/cforth/toys/blob/master/sort/heap_sort.py)  
6. [快速排序算法](https://github.com/cforth/toys/blob/master/sort/quick_sort.py)  
7. [计数排序算法](https://github.com/cforth/toys/blob/master/sort/counting_sort.py)  
8. [基数排序算法](https://github.com/cforth/toys/blob/master/sort/radix_sort.py)  

graphs
-------------
图的数据结构与算法。  
1. [无向图的邻接列表表示](https://github.com/cforth/toys/blob/master/graphs/undirected_graphs.py)    
2. [深度优先算法](https://github.com/cforth/toys/blob/master/graphs/depth_first_search.py)   
3. [深度优先路径查询](https://github.com/cforth/toys/blob/master/graphs/depth_first_paths.py)  

search
-------------
常用的搜索算法的演示代码。  
1. [二叉搜索树的实现](https://github.com/cforth/toys/blob/master/search/binary_search_tree.py)  
2. [深度与广度优先遍历](https://github.com/cforth/toys/blob/master/search/tree_ergodic.py)


search/print_tree
-------------
一个外国牛人写的[小工具](https://github.com/cforth/toys/tree/master/search/print_tree)，打印出树结构图（C语言）。


Simple
-------------
[《计算的本质：深入剖析程序和计算机》](http://www.ituring.com.cn/book/1098)中第二章的Simple语言实现。  
1. [小步操作语义-表达式](https://github.com/cforth/toys/blob/master/Simple/Machine2.3.1-1.py)    
2. [小步操作语义-语句](https://github.com/cforth/toys/blob/master/Simple/Machine2.3.1-2.py)   
3. [大步操作语义](https://github.com/cforth/toys/blob/master/Simple/Evaluate2.3.2.py)  
4. [指称语义](https://github.com/cforth/toys/blob/master/Simple/Denotation2.4.py)


Automaton
-------------
[《计算的本质：深入剖析程序和计算机》](http://www.ituring.com.cn/book/1098)中第三章以及第四章的自动机实现。  
1. [确定性有限自动机（Deterministic Finite Automaton，DFA）](https://github.com/cforth/toys/blob/master/Automaton/DFA3.1.py)  
2. [非确定性有限自动机（Nondeterministic Finite Automata，NFA）](https://github.com/cforth/toys/blob/master/Automaton/NFA3.2.py)  
3. [正则表达式的实现](https://github.com/cforth/toys/blob/master/Automaton/Pattern3.3.py)  
4. [NFA与DFA的等价性](https://github.com/cforth/toys/blob/master/Automaton/NFASimulation3.4.py)  
5. [确定性下推自动机（Deterministic PushDown Automaton，DPDA）](https://github.com/cforth/toys/blob/master/Automaton/DPDA4.1.py)  
6. [非确定性下推自动机（Nondeterministic Pushdown Automaton，NPDA）](https://github.com/cforth/toys/blob/master/Automaton/NPDA4.2.py)  
7. [词法分析（Lexical Analyzer）](https://github.com/cforth/toys/blob/master/Automaton/LexicalAnalyzer4.3.1.py)  
8. [语法分析（Grammar Analyzer）](https://github.com/cforth/toys/blob/master/Automaton/GrammarAnalyzer4.3.2.py)


Turing
-------------
[《计算的本质：深入剖析程序和计算机》](http://www.ituring.com.cn/book/1098)中第五章的图灵机实现。   
1. [确定型图灵机（Deterministic Turing Machine，DTM）](https://github.com/cforth/toys/blob/master/Turing/DTM.py)    


LambdaCalculus
---------------
[《计算的本质：深入剖析程序和计算机》](http://www.ituring.com.cn/book/1098)中第六章、第七章的Lambda演算实现。   
1. [模拟lambda演算](https://github.com/cforth/toys/blob/master/LambdaCalculus/lambda6.1.py)    
2. [FizzBuzz游戏(0-50)](https://github.com/cforth/toys/blob/master/LambdaCalculus/FizzBuzz.py)  
3. [lambda演算](https://github.com/cforth/toys/blob/master/LambdaCalculus/LambdaCalculus7.1.py)  
