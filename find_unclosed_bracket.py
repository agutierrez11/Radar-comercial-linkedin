import sys

with open('temp_script7.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

stack = []
for line_num, line in enumerate(lines, 1):
    for char_num, char in enumerate(line, 1):
        if char in '({[':
            stack.append((char, line_num, char_num))
        elif char in ')}]' :
            if not stack:
                print(f"Unmatched closing '{char}' at line {line_num}:{char_num}")
            else:
                top, top_line, top_char = stack.pop()
                expected = {'(': ')', '{': '}', '[': ']'}[top]
                if char != expected:
                    print(f"Mismatched '{char}' at line {line_num}:{char_num}, expected '{expected}' opened at line {top_line}:{top_char}")

print(f"\nRemaining unclosed brackets count: {len(stack)}")
for item in stack[-10:]:
    print(f"Unclosed '{item[0]}' opened at line {item[1]}:{item[2]}")
