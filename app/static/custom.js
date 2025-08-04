// 自定义样式注入脚本
(function() {
    'use strict';
    
    // 等待页面加载完成
    function waitForElement(selector, callback) {
        if (document.querySelector(selector)) {
            callback();
        } else {
            setTimeout(function() {
                waitForElement(selector, callback);
            }, 100);
        }
    }
    
    // 应用自定义样式
    function applyCustomStyles() {
        // 创建样式元素
        const style = document.createElement('style');
        style.textContent = `
            /* 自定义API文档样式 - 优化中文显示和紧凑布局 */
            
            /* 整体容器优化 */
            .swagger-ui {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", Helvetica, Arial, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 10px;
            }
            
            /* 标题栏优化 */
            .swagger-ui .topbar {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 10px 20px;
                border-radius: 8px;
                margin-bottom: 20px;
            }
            
            .swagger-ui .topbar .download-url-wrapper {
                margin: 10px 0;
            }
            
            /* 操作面板优化 */
            .swagger-ui .opblock {
                margin-bottom: 15px;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            
            .swagger-ui .opblock .opblock-summary {
                padding: 12px 15px;
                border-radius: 8px 8px 0 0;
            }
            
            .swagger-ui .opblock .opblock-summary-method {
                min-width: 80px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 4px;
            }
            
            .swagger-ui .opblock .opblock-summary-path {
                font-size: 14px;
                font-weight: 500;
            }
            
            .swagger-ui .opblock .opblock-summary-description {
                font-size: 13px;
                color: #666;
            }
            
            /* 标签页优化 */
            .swagger-ui .opblock-tag {
                margin-bottom: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            
            .swagger-ui .opblock-tag .opblock-tag-section {
                padding: 15px;
            }
            
            .swagger-ui .opblock-tag .opblock-tag-section h3 {
                font-size: 16px;
                font-weight: 600;
                color: #333;
                margin: 0 0 10px 0;
            }
            
            /* 参数表格优化 */
            .swagger-ui .parameters-container {
                margin: 15px 0;
            }
            
            .swagger-ui .parameters-container .parameters {
                font-size: 13px;
            }
            
            .swagger-ui .parameters-container .parameters th {
                background: #f8f9fa;
                font-weight: 600;
                padding: 8px 12px;
            }
            
            .swagger-ui .parameters-container .parameters td {
                padding: 8px 12px;
                vertical-align: top;
            }
            
            /* 响应区域优化 */
            .swagger-ui .responses-wrapper {
                margin: 15px 0;
            }
            
            .swagger-ui .responses-wrapper .responses-inner {
                font-size: 13px;
            }
            
            /* 模型定义优化 */
            .swagger-ui .model {
                font-size: 13px;
                margin: 10px 0;
            }
            
            .swagger-ui .model .model-title {
                font-weight: 600;
                color: #333;
            }
            
            /* 按钮优化 */
            .swagger-ui .btn {
                border-radius: 4px;
                font-size: 12px;
                padding: 6px 12px;
                font-weight: 500;
            }
            
            .swagger-ui .btn.execute {
                background: #28a745;
                border-color: #28a745;
            }
            
            .swagger-ui .btn.execute:hover {
                background: #218838;
                border-color: #1e7e34;
            }
            
            /* 输入框优化 */
            .swagger-ui .parameter__name {
                font-weight: 600;
                color: #333;
            }
            
            .swagger-ui .parameter__type {
                color: #666;
                font-size: 12px;
            }
            
            .swagger-ui .parameter__deprecated {
                color: #dc3545;
                font-size: 12px;
            }
            
            /* 描述文本优化 */
            .swagger-ui .opblock-description-wrapper {
                font-size: 13px;
                line-height: 1.5;
                color: #555;
            }
            
            /* 代码块优化 */
            .swagger-ui .microlight {
                font-size: 12px;
                background: #f8f9fa;
                border-radius: 4px;
                padding: 8px;
            }
            
            /* 标签页导航优化 */
            .swagger-ui .tab-header {
                background: #f8f9fa;
                border-radius: 4px;
                margin-bottom: 15px;
            }
            
            .swagger-ui .tab-header .tab-item {
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 500;
            }
            
            .swagger-ui .tab-header .tab-item.active {
                background: #007bff;
                color: white;
                border-radius: 4px;
            }
            
            /* 响应状态码优化 */
            .swagger-ui .response-col_status {
                font-weight: 600;
                font-size: 12px;
            }
            
            .swagger-ui .response-col_status.response-200 {
                color: #28a745;
            }
            
            .swagger-ui .response-col_status.response-400,
            .swagger-ui .response-col_status.response-404,
            .swagger-ui .response-col_status.response-500 {
                color: #dc3545;
            }
            
            /* 紧凑模式优化 */
            .swagger-ui .opblock .opblock-summary {
                padding: 8px 12px;
            }
            
            .swagger-ui .opblock .opblock-summary-path {
                font-size: 13px;
            }
            
            .swagger-ui .opblock .opblock-summary-description {
                font-size: 12px;
            }
            
            /* 中文标签优化 */
            .swagger-ui .opblock-tag .opblock-tag-section h3 {
                font-size: 15px;
                font-weight: 600;
                color: #2c3e50;
            }
            
            /* 滚动条优化 */
            .swagger-ui ::-webkit-scrollbar {
                width: 6px;
                height: 6px;
            }
            
            .swagger-ui ::-webkit-scrollbar-track {
                background: #f1f1f1;
                border-radius: 3px;
            }
            
            .swagger-ui ::-webkit-scrollbar-thumb {
                background: #c1c1c1;
                border-radius: 3px;
            }
            
            .swagger-ui ::-webkit-scrollbar-thumb:hover {
                background: #a8a8a8;
            }
            
            /* 响应式优化 */
            @media (max-width: 768px) {
                .swagger-ui {
                    padding: 5px;
                }
                
                .swagger-ui .opblock .opblock-summary-path {
                    font-size: 12px;
                }
                
                .swagger-ui .opblock .opblock-summary-description {
                    font-size: 11px;
                }
            }
            
            /* 暗色主题支持 */
            @media (prefers-color-scheme: dark) {
                .swagger-ui {
                    background: #1a1a1a;
                    color: #e0e0e0;
                }
                
                .swagger-ui .opblock {
                    background: #2d2d2d;
                    border: 1px solid #404040;
                }
                
                .swagger-ui .parameters-container .parameters th {
                    background: #404040;
                    color: #e0e0e0;
                }
                
                .swagger-ui .parameters-container .parameters td {
                    color: #e0e0e0;
                }
            }
        `;
        
        // 添加到页面头部
        document.head.appendChild(style);
        
        console.log('自定义样式已应用');
    }
    
    // 等待Swagger UI加载完成后应用样式
    waitForElement('.swagger-ui', function() {
        // 延迟一点时间确保样式完全加载
        setTimeout(applyCustomStyles, 500);
    });
    
    // 如果页面已经加载完成，直接应用样式
    if (document.readyState === 'complete') {
        waitForElement('.swagger-ui', applyCustomStyles);
    } else {
        window.addEventListener('load', function() {
            waitForElement('.swagger-ui', applyCustomStyles);
        });
    }
})(); 