from analyzer.analyzer import analyze_code

def test_lines_of_code():
    code = "print('Hello')"
    result = analyze_code(code)
    assert result["lines_of_code"] == 1