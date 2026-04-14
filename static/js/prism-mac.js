/**
 * Prism.js Mac 风格增强
 * 提供自定义复制按钮和语言显示功能
 */

// 注册自定义复制按钮
Prism.plugins.toolbar.registerButton('copy-to-clipboard', {
    text: 'Copy',
    onClick: function(env) {
        // 获取代码文本
        const code = env.element.textContent;

        // 复制到剪贴板
        navigator.clipboard.writeText(code).then(() => {
            // 成功反馈
            const button = this.element.querySelector('button') || this.element;
            const originalText = button.textContent;

            button.textContent = 'Copied!';
            button.style.background = 'rgba(39, 201, 63, 0.2)';
            button.style.color = '#27c93f';
            button.style.borderColor = '#27c93f';

            setTimeout(() => {
                button.textContent = originalText;
                button.style.background = '';
                button.style.color = '';
                button.style.borderColor = '';
            }, 2000);
        }).catch(err => {
            console.error('复制失败:', err);
            const button = this.element.querySelector('button') || this.element;
            button.textContent = 'Failed';

            setTimeout(() => {
                button.textContent = 'Copy';
            }, 2000);
        });
    }
});

// 页面加载完成后高亮所有代码
document.addEventListener('DOMContentLoaded', function() {
    // 重新高亮所有代码块
    Prism.highlightAll();

    // 自动为没有代码块的 pre 标签添加语言标记
    document.querySelectorAll('pre:not([class*="language-"])').forEach(pre => {
        pre.classList.add('language-plaintext');
    });
});

// 监听动态添加的内容（适用于 AJAX 或 SPA）
const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        if (mutation.addedNodes) {
            mutation.addedNodes.forEach(function(node) {
                if (node.querySelectorAll) {
                    const codeBlocks = node.querySelectorAll('pre code');
                    codeBlocks.forEach(function(block) {
                        Prism.highlightElement(block);
                    });
                }
            });
        }
    });
});

// 开始观察整个文档
observer.observe(document.body, {
    childList: true,
    subtree: true
});
