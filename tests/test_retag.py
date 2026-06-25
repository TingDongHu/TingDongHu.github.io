# tests/test_retag.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from retag import apply_tag_map, rewrite_tags_line


def test_apply_rename_and_merge():
    # c++ 与 C++ 合并到 C++;扩散模型/文生图 合并到 Diffusion
    tags = ["c++", "C++", "扩散模型", "文生图", "语法"]
    rename = {"c++": "C++", "扩散模型": "Diffusion", "文生图": "Diffusion"}
    delete = []
    assert apply_tag_map(tags, rename, delete) == ["C++", "Diffusion", "语法"]


def test_apply_delete_and_dedupe():
    tags = ["入门", "环境配置", "LLM", "LLM"]
    rename = {}
    delete = ["入门", "环境配置"]
    assert apply_tag_map(tags, rename, delete) == ["LLM"]


def test_unmapped_kept_in_order():
    tags = ["A", "B", "C"]
    assert apply_tag_map(tags, {}, []) == ["A", "B", "C"]


def test_rewrite_tags_line_basic():
    line = 'tags: ["排序算法", "冒泡排序", "插入排序"]'
    rename = {"冒泡排序": "排序算法", "插入排序": "排序算法"}
    out = rewrite_tags_line(line, rename, [])
    assert out == 'tags: ["排序算法"]'


def test_rewrite_preserves_single_quotes_input():
    # 兼容单引号或空格变体输入,输出统一双引号
    line = "tags: ['LLM', 'NLP']"
    out = rewrite_tags_line(line, {}, [])
    assert out == 'tags: ["LLM", "NLP"]'


def test_rewrite_empty_after_delete():
    line = 'tags: ["入门"]'
    out = rewrite_tags_line(line, {}, ["入门"])
    assert out == 'tags: []'


from retag import find_tags_line


def test_find_tags_line_in_frontmatter():
    text = '---\ntitle: 测试\ntags: ["A", "B"]\ndate: 2025\n---\n正文 tags: 不该匹配\n'
    assert find_tags_line(text) == 'tags: ["A", "B"]'


def test_find_tags_line_none_when_absent():
    text = '---\ntitle: 无标签\n---\n正文\n'
    assert find_tags_line(text) is None


def test_find_tags_line_ignores_body():
    # 正文里出现 tags: 不在首个 --- 块内,不该被当成 front matter tags
    text = '---\ntitle: x\n---\n这里写 tags: ["假"]\n'
    assert find_tags_line(text) is None


import tempfile
from retag import process_file


def test_process_file_dryrun_no_write():
    content = '---\ntitle: t\ntags: ["c++", "语法"]\ndate: 2025\n---\n正文\n'
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(content)
        path = f.name
    try:
        old, new = process_file(path, {"c++": "C++"}, [], apply=False)
        assert old == 'tags: ["c++", "语法"]'
        assert new == 'tags: ["C++", "语法"]'
        assert open(path, encoding="utf-8").read() == content
    finally:
        os.unlink(path)


def test_process_file_apply_writes():
    content = '---\ntitle: t\ntags: ["c++", "语法"]\n---\n正文\n'
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(content)
        path = f.name
    try:
        process_file(path, {"c++": "C++"}, [], apply=True)
        after = open(path, encoding="utf-8").read()
        assert 'tags: ["C++", "语法"]' in after
        assert "正文" in after
        assert "title: t" in after
    finally:
        os.unlink(path)


def test_process_file_no_change_returns_none():
    content = '---\ntags: ["LLM"]\n---\n'
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(content)
        path = f.name
    try:
        assert process_file(path, {}, [], apply=False) is None
    finally:
        os.unlink(path)
