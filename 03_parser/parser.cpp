#include <iostream>
#include <vector>
#include <string>

int eval_op(int a, int b, char op) 
{
    if (op == '+') return a + b;
    if (op == '-') return a - b;
    if (op == '*') return a * b;
    if (op == '/') return a / b; // Integer division
    return 0;
}

int precedence(char op) 
{
    if (op == '+' || op == '-') return 1;
    if (op == '*' || op == '/') return 2;
    return 0;
}

void read_eval(std::vector<int>* numbers, std::vector<char>* operators)
{
    int right = numbers->back(); numbers->pop_back();
    int left = numbers->back(); numbers->pop_back();
    numbers->push_back(eval_op(left, right, operators->back()));
    operators->pop_back();   
}

int eval(const std::string& exp) 
{
    std::vector<int> numbers;
    std::vector<char> operators;
    std::string digits_str = "";

    for (int i = 0; i < exp.length(); ++i) 
    {
        // Current char processed
        char c = exp[i]; 

        // Skip spaces
        if (c == ' ') continue;

        // If left parenthesis, add and continue
        if (c == '(') 
        {
            operators.push_back(c);
            continue;
        }

        // If digit, append to digit stack
        if (isdigit(c)) 
        {
            digits_str += c;

            // Check if is the last digit in the sequence
            if (i + 1 > exp.length() - 1 || !isdigit(exp[i + 1])) 
            {
                numbers.push_back(std::stoi(digits_str));
                digits_str = "";
            }
            continue;
        }

        // If right parenthesis, load operators until left parenthesis
        if (c == ')') 
        {
            while (!operators.empty() && operators.back() != '(') 
                read_eval(&numbers, &operators);

            // Discard the left parenthesis
            operators.pop_back();
            continue;
        }

        // Otherwise, operator found. Check if it has lower precendece
        while (!operators.empty() && precedence(operators.back()) >= precedence(c)) 
            read_eval(&numbers, &operators);

        // If not, higer precendece detected
        operators.push_back(c);
    }

    // Clear the stack
    while (!operators.empty())
        read_eval(&numbers, &operators);

    // Return value
    return numbers.back();
}

int main() 
{
    while (true)
    {
        char exp[100];
        std::cout << "Type expression: ";
        std::cin.getline(exp, 100);
        std::cout << "Result: " << eval(exp) << "\n";
    }
    return 0;
}
