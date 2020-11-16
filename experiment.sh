#!/bin/sh

# for ((i=0;i<1000;i++))
# do
# 	python3 non_uniform.py input_nonuniform/input_61.dat input_nonuniform/input_62.dat
# 	python3 solve.py input_nonuniform/input_61.dat input_nonuniform/input_62.dat
# done
# echo "Finish!"

# for ((i=0;i<1000;i++))
# do
# 	python3 non_uniform_1000.py input_nonuniform/input_61.dat input_nonuniform/input_62.dat
# 	python3 solve.py input_nonuniform/input_61.dat input_nonuniform/input_62.dat
# 	echo $i
# done
# echo "Finish!"

# for ((i=0;i<1000;i++))
# do
# 	python3 uniform.py input_uniform/input_61.dat input_uniform/input_62.dat
# 	python3 solve.py input_uniform/input_61.dat input_uniform/input_62.dat
# done
# echo "Finish!"

# for ((i=0;i<1000;i++))
# do
# 	python3 uniform_1000.py input_uniform/input_61.dat input_uniform/input_62.dat
# 	python3 solve.py input_uniform/input_61.dat input_uniform/input_62.dat
# done
# echo "Finish!"

# for ((i=0;i<1000;i++))
# do
# 	python3 uniform_10000.py input_uniform/input_61.dat input_uniform/input_62.dat
# 	python3 solve.py input_uniform/input_61.dat input_uniform/input_62.dat
# done
# echo "Finish!"

# for ((i=1;i<61;i+=2))
# do
# 	j=$(($i+1))
# 	echo $j
# 	python3 solve.py input_uniform/input_$i.dat input_uniform/input_$j.dat
# done
# echo "Finish!"

# for ((i=2000;i<4000;i+=2))
# do
# 	j=$(($i+1))
# 	python3 uniform.py input_1116/input_$i.dat input_1116/input_$j.dat
# 	python3 solve.py input_1116/input_$i.dat input_1116/input_$j.dat output_1116/output_$i.dat
# 	echo $i
# done
# echo "Finish!"