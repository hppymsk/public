#Project Euler Problems

import math
import time

class Euler:
    def __init__(self):
        self.solved_problems = 4
        self.description = ''
        self.answer = 0

    def all_answers(self):
        for i in range(1, self.solved_problems+1):
            answer = 'problem_' + str(i)
            print('Problem ', i, ': ', getattr(self, answer)(), sep='')
        return
    
    #accepts an integer and returns True if it is prime
    def isitprime(self, n):
        if (n <= 1) :
            return False
        if (n <= 3) :
            return True
        if (n % 2 == 0 or n % 3 == 0) :
            return False
        i = 5
        while(i * i <= n) :
            if (n % i == 0 or n % (i + 2) == 0) :
                return False
            i = i + 6
        return True
    
    #accepts an integer and returns a list of primes of n length
    def primelist(self, howmany):
        listofprimes = []
        i = 1
        while len(listofprimes) < howmany:
            if self.isitprime(i):
                listofprimes.append(i)
            i += 1
        #for i in range(1, howmany):
        #    if self.isitprime(i):
        #        listofprimes.append(i)
        return listofprimes

    def stringreverse(self, s):
        s = str(s)
        s = list(s)
        r = ''
        for i in range(len(s)-1, -1, -1):
            #r.append(s[i])
            r += s[i]
        return r

    def problem_1(self):
        self.description = ('If we list all the natural numbers below 10 that are '
                       'multiples of 3 or 5, we get 3, 5, 6 and 9. '
                       'The sum of these multiples is 23. Find the sum of all the multiples of 3 or 5 below 1000.')
        self.answer = 233168
        
        sumlist = []
        for i in range(3, 1000):
            if i % 3 == 0 or i % 5 == 0:
                sumlist.append(i)

        return sum(sumlist)

    def problem_2(self):
        self.description = ('Each new term in the Fibonacci sequence is generated by adding the previous two terms. By starting with 1 and 2, the first 10 terms will be:'
                            '1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ...'
                            'By considering the terms in the Fibonacci sequence whose values do not exceed four million, find the sum of the even-valued terms.')
        self.answer = 4613732
        fibb1 = 1
        fibb2 = 2
        fibblist = []
        while True:
            if fibb1 >= 4000000:
                break
            fibblist.append(fibb1)
            fibbnew = fibb1
            fibb1 = fibb2
            fibb2 = fibbnew + fibb2
        fibbeven = []
        for i in range(1, len(fibblist)):
            if fibblist[i] % 2 == 0:
                fibbeven.append(fibblist[i])
        
        return sum(fibbeven)
    
    def problem_3(self):
        self.description = ('The prime factors of 13195 are 5, 7, 13 and 29.'
                            'What is the largest prime factor of the number 600851475143 ?')
        self.answer = 6857
        primefactor = []
        num = 600851475143
        prime = self.primelist(100000)
        for i in range(0, len(prime)):
            if num % prime[i] == 0:
                primefactor.append(prime[i])
        print(primefactor)
        return primefactor
    
    def problem_4(self):
        self.description = ('A palindromic number reads the same both ways. The largest palindrome made from the product of two 2-digit numbers is 9009 = 91 × 99.'
                            'Find the largest palindrome made from the product of two 3-digit numbers.')
        self.answer = 906609
        palindrome = 0
        for i in range(100, 1000):
            for j in range(100, 1000):
                x = i * j
                y = int(self.stringreverse(x))
                if x == y and x >= palindrome:
                    palindrome = x
        return palindrome
    
    def problem_5(self):
        self.description = ('2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.'
                            'What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?')
        self.answer = 232792560

        i = 0
        divisible = True
        while True:
            i += 20
            divisible = True
            for x in range(2, 20):
                if i % x != 0:
                    divisible = False
                    break
            if divisible == True:
                break
        return i

    def problem_6(self):
        self.description = ('The sum of the squares of the first ten natural numbers is, 385'
                            'The square of the sum of the first ten natural numbers is, 3025'
                            'Hence the difference between the sum of the squares of the first ten natural numbers and the square of the sum is .'
                            'Find the difference between the sum of the squares of the first one hundred natural numbers and the square of the sum.')
        self.answer = 25164150
        sumofsquare = 0
        squareofsum = 0
        for i in range(1, 101):
            sumofsquare += i ** 2
        for i in range (1,101):
            squareofsum += i
        squareofsum = squareofsum ** 2
        difference = abs(sumofsquare - squareofsum)
        
        return difference
    
    def problem_7(self):
        self.description = ('What is the 10001st prime number')
        self.answer = 104743
        prime = self.primelist(10001)
        
        return prime[-1]
    
    def problem_8(self):
        self.description = ('The four adjacent digits in the 1000-digit number that have the greatest product are 9 × 9 × 8 × 9 = 5832.'
                            'Find the thirteen adjacent digits in the 1000-digit number that have the greatest product. What is the value of this product?')
        self.answer = 23514624000
        digit = '7316717653133062491922511967442657474235534919493496983520312774506326239578318016984801869478851843858615607891129494954595017379583319528532088055111254069874715852386305071569329096329522744304355766896648950445244523161731856403098711121722383113622298934233803081353362766142828064444866452387493035890729629049156044077239071381051585930796086670172427121883998797908792274921901699720888093776657273330010533678812202354218097512545405947522435258490771167055601360483958644670632441572215539753697817977846174064955149290862569321978468622482839722413756570560574902614079729686524145351004748216637048440319989000889524345065854122758866688116427171479924442928230863465674813919123162824586178664583591245665294765456828489128831426076900422421902267105562632111110937054421750694165896040807198403850962455444362981230987879927244284909188845801561660979191338754992005240636899125607176060588611646710940507754100225698315520005593572972571636269561882670428252483600823257530420752963450'
        digit = list(digit)
        highest = 0
        for x in range((len(digit)-12)):
            multiply = 1
            for y in range(0,13):
                multiply *= int(digit[x+y])
            if multiply > highest:
                highest = multiply
        return highest
    
    def problem_9(self):
        self.description = ('A Pythagorean triplet is a set of three natural numbers, a < b < c, for which, a2 + b2 = c2. For example, 32 + 42 = 9 + 16 = 25 = 52. '
                            'There exists exactly one Pythagorean triplet for which a + b + c = 1000. Find the product abc.')
        self.answer = 31875000
        product = 0
        for a in range(1,1000):
            for b in range(2,1000):
                c = math.sqrt(a ** 2 + b ** 2)
                if a < b and b < c and a + b + c == 1000:
                    product = a * b * c
        return product

    def problem_10(self):
        self.description = ('The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.'
                            'Find the sum of all the primes below two million.')
        self.answer = 142913828922
        listofprimes = []
        i = 1
        for i in range(1, 2000000):
            if self.isitprime(i):
                listofprimes.append(i)
        return sum(listofprimes)

    def problem_11(self):
        self.description = ('In the 20×20 grid below, four numbers along a diagonal line have been marked in red.'
                            'The product of these numbers is 26 × 63 × 78 × 14 = 1788696.'
                            'What is the greatest product of four adjacent numbers in the same direction (up, down, left, right, or diagonally) in the 20×20 grid?')
        self.answer = 70600674

        grid = [[8, 2, 22, 97, 38, 15, 0, 40, 0, 75, 4, 5, 7, 78, 52, 12, 50, 77, 91, 8],
                [49, 49, 99, 40, 17, 81, 18, 57, 60, 87, 17, 40, 98, 43, 69, 48, 4, 56, 62, 0],
                [81, 49, 31, 73, 55, 79, 14, 29, 93, 71, 40, 67, 53, 88, 30, 3, 49, 13, 36, 65],
                [52, 70, 95, 23, 4, 60, 11, 42, 69, 24, 68, 56, 1, 32, 56, 71, 37, 2, 36, 91],
                [22, 31, 16, 71, 51, 67, 63, 89, 41, 92, 36, 54, 22, 40, 40, 28, 66, 33, 13, 80],
                [24, 47, 32, 60, 99, 3, 45, 2, 44, 75, 33, 53, 78, 36, 84, 20, 35, 17, 12, 50],
                [32, 98, 81, 28, 64, 23, 67, 10, 26, 38, 40, 67, 59, 54, 70, 66, 18, 38, 64, 70],
                [67, 26, 20, 68, 2, 62, 12, 20, 95, 63, 94, 39, 63, 8, 40, 91, 66, 49, 94, 21],
                [24, 55, 58, 5, 66, 73, 99, 26, 97, 17, 78, 78, 96, 83, 14, 88, 34, 89, 63, 72],
                [21, 36, 23, 9, 75, 0, 76, 44, 20, 45, 35, 14, 0, 61, 33, 97, 34, 31, 33, 95],
                [78, 17, 53, 28, 22, 75, 31, 67, 15, 94, 3, 80, 4, 62, 16, 14, 9, 53, 56, 92],
                [16, 39, 5, 42, 96, 35, 31, 47, 55, 58, 88, 24, 0, 17, 54, 24, 36, 29, 85, 57],
                [86, 56, 0, 48, 35, 71, 89, 7, 5, 44, 44, 37, 44, 60, 21, 58, 51, 54, 17, 58],
                [19, 80, 81, 68, 5, 94, 47, 69, 28, 73, 92, 13, 86, 52, 17, 77, 4, 89, 55, 40],
                [4, 52, 8, 83, 97, 35, 99, 16, 7, 97, 57, 32, 16, 26, 26, 79, 33, 27, 98, 66],
                [88, 36, 68, 87, 57, 62, 20, 72, 3, 46, 33, 67, 46, 55, 12, 32, 63, 93, 53, 69],
                [4, 42, 16, 73, 38, 25, 39, 11, 24, 94, 72, 18, 8, 46, 29, 32, 40, 62, 76, 36],
                [20, 69, 36, 41, 72, 30, 23, 88, 34, 62, 99, 69, 82, 67, 59, 85, 74, 4, 36, 16],
                [20, 73, 35, 29, 78, 31, 90, 1, 74, 31, 49, 71, 48, 86, 81, 16, 23, 57, 5, 54],
                [1, 70, 54, 71, 83, 51, 54, 69, 16, 92, 33, 48, 61, 43, 52, 1, 89, 19, 67, 48]]
        mult = 1
        biggest = 0

        #right
        for x in range(20):
            for y in range(17):
                mult = []
                for z in range(4):
                    mult.append(grid[x][y+z])
                #print(mult)
                product = math.prod(mult)
                if  product > biggest:
                    biggest = product
        
        #down
        for x in range(17):
            for y in range(20):
                mult = []
                for z in range(4):
                    mult.append(grid[x+z][y])
                #print(mult)
                product = math.prod(mult)
                if  product > biggest:
                    biggest = product
        

        #right diagonal
        for x in range(17):
            for y in range(17):
                mult = []
                a = 0
                for z in range(4):
                    mult.append(grid[x+a][y+z])
                    a += 1
                #print(mult)
                product = math.prod(mult)
                if  product > biggest:
                    biggest = product

        #left diagonal
        for x in range(17):
            for y in range(3,20):
                mult = []
                a = 0
                for z in range(4):
                    mult.append(grid[x+z][y-a])
                    a += 1
                #print(mult)
                product = math.prod(mult)
                if  product > biggest:
                    biggest = product

        
        return biggest                

    def problem_12(self):
        self.description = ('What is the value of the first triangle number to have over five hundred divisors?')
        self.answer = 76576500
        x = 0
        while True:
            x += 1
            triangle = 0
            for y in range(1, x):
                triangle += y
            
            divisor = []
            for z in range(1, int(math.sqrt(triangle))):
                if triangle % z == 0:
                    divisor.append(z)
            if len(divisor) * 2 > 500:
                return triangle
    
    def problem_13(self):
        self.description = ('Work out the first ten digits of the sum of the following one-hundred 50-digit numbers.')
        self.answer = 5537376230

        with open('problem13nums.txt') as f:
            data = [line.rstrip() for line in f]
        
        total = 0

        for i in range(100):
            total += int(data[i])
        
        return total

    def problem_14(self):
        self.description('')


def main():
    E = Euler()

    print(E.problem_13())

if __name__ == '__main__':
    main()