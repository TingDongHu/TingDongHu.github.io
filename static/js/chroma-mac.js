/**
 * Hugo Chroma Mac 风格增强
 * 为代码块添加 Mac 三色圆点和复制功能
 */

document.addEventListener('DOMContentLoaded', function() {
    // 为所有代码块添加 Mac 三色圆点
    document.querySelectorAll('.highlight').forEach(function(block) {
        // 检查是否已经有圆点了
        if (block.querySelector('.mac-dots')) {
            return;
        }

        // 创建圆点容器
        var dotsContainer = document.createElement('div');
        dotsContainer.className = 'mac-dots';

        // 创建三个圆点
        var redDot = document.createElement('span');
        redDot.className = 'dot-red';

        var yellowDot = document.createElement('span');
        yellowDot.className = 'dot-yellow';

        var greenDot = document.createElement('span');
        greenDot.className = 'dot-green';

        // 添加圆点到容器
        dotsContainer.appendChild(redDot);
        dotsContainer.appendChild(yellowDot);
        dotsContainer.appendChild(greenDot);

        // 将圆点容器添加到代码块（在 chroma div 之前）
        var chromaDiv = block.querySelector('.chroma');
        if (chromaDiv) {
            block.insertBefore(dotsContainer, chromaDiv);
        } else {
            block.insertBefore(dotsContainer, block.firstChild);
        }
    });

    // 为所有代码块添加复制按钮（只在代码内容td中）
    document.querySelectorAll('.highlight td.lntd:last-child').forEach(function(tdElement) {
        // 检查是否已经有复制按钮了
        if (tdElement.querySelector('.mac-copy-btn')) {
            return;
        }

        // 找到代码内容
        var preElement = tdElement.querySelector('pre');
        if (!preElement) return;

        var codeElement = preElement.querySelector('code') || preElement;

        // 创建工具栏容器
        var toolbarContainer = document.createElement('div');
        toolbarContainer.className = 'mac-toolbar';

        // 添加语言标签
        var languageClass = preElement.className.match(/language-(\w+)/);
        if (languageClass) {
            var languageLabel = document.createElement('div');
            languageLabel.className = 'mac-language';
            languageLabel.textContent = languageClass[1];
            toolbarContainer.appendChild(languageLabel);
        }

        // 创建复制按钮
        var copyButton = document.createElement('button');
        copyButton.type = 'button';
        copyButton.className = 'mac-copy-btn';
        copyButton.textContent = 'Copy';

        copyButton.addEventListener('click', function() {
            var codeText = codeElement.textContent;

            navigator.clipboard.writeText(codeText).then(function() {
                var originalText = copyButton.textContent;
                copyButton.textContent = 'Copied!';
                copyButton.style.background = 'rgba(39, 201, 63, 0.2)';
                copyButton.style.color = '#27c93f';
                copyButton.style.borderColor = '#27c93f';

                setTimeout(function() {
                    copyButton.textContent = originalText;
                    copyButton.style.background = '';
                    copyButton.style.color = '';
                    copyButton.style.borderColor = '';
                }, 2000);
            }).catch(function(err) {
                console.error('复制失败:', err);
                copyButton.textContent = 'Failed';

                setTimeout(function() {
                    copyButton.textContent = 'Copy';
                }, 2000);
            });
        });

        toolbarContainer.appendChild(copyButton);

        // 将工具栏添加到 td 的最前面
        tdElement.insertBefore(toolbarContainer, tdElement.firstChild);
    });

    // 移除重复的 code-toolbar（如果有）
    document.querySelectorAll('.highlight .code-toolbar').forEach(function(toolbar) {
        toolbar.remove();
    });
});
