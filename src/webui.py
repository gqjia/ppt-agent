import gradio as gr
from smolagents import stream_to_gradio, MessageRole
from phoenix.otel import register
from openinference.instrumentation.smolagents import SmolagentsInstrumentor

from .agents.ppt_generate import ppt_generate_agent


class PPTGeneratorUI:
    """
    美观的PPT生成器Gradio界面
    
    这个类提供了一个现代化、美观的Web界面来与PPT生成agent交互，
    支持实时聊天和PPT生成功能。
    """

    def __init__(self, agent, reset_agent_memory: bool = False):
        self.agent = agent
        self.reset_agent_memory = reset_agent_memory
        self.name = "AI PPT生成器"
        self.description = "基于AI的智能PPT生成工具，支持主题输入和内容生成"

    def interact_with_agent(self, prompt, messages, session_state):
        """与 agent 交互的核心方法"""
        if "agent" not in session_state:
            session_state["agent"] = self.agent

        try:
            messages.append(gr.ChatMessage(role="user", content=prompt, metadata={"status": "done"}))
            yield messages

            for msg in stream_to_gradio(
                session_state["agent"], task=prompt, reset_agent_memory=self.reset_agent_memory
            ):
                if isinstance(msg, gr.ChatMessage):
                    messages[-1].metadata["status"] = "done"
                    messages.append(msg)
                elif isinstance(msg, str):
                    msg = msg.replace("<", r"\<").replace(">", r"\>")
                    if messages[-1].metadata["status"] == "pending":
                        messages[-1].content = msg
                    else:
                        messages.append(
                            gr.ChatMessage(role=MessageRole.ASSISTANT, content=msg, metadata={"status": "pending"})
                        )
                yield messages

            yield messages
        except Exception as e:
            yield messages
            raise gr.Error(f"交互过程中发生错误: {str(e)}")

    def create_app(self):
        """创建Gradio应用"""
        # 美观简洁的CSS样式
        custom_css = """
        .main-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }
        .chat-container {
            border: none;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            background: white;
            overflow: hidden;
        }
        .chat-container .message {
            font-size: 16px !important;
            line-height: 1.5 !important;
            padding: 8px 12px !important;
            margin: 6px 0 !important;
            border-radius: 8px !important;
        }
        .chat-container .message-content {
            font-size: 16px !important;
            line-height: 1.5 !important;
            padding: 6px 10px !important;
        }
        .chat-container p {
            font-size: 16px !important;
            line-height: 1.5 !important;
            margin-bottom: 10px !important;
            padding: 0 !important;
        }
        .chat-container .message-bubble {
            padding: 8px 12px !important;
            margin: 4px 0 !important;
            border-radius: 8px !important;
        }
        /* Agent消息样式优化 */
        .chat-container .message[data-role="assistant"] {
            background: linear-gradient(135deg, #f8f9ff 0%, #e8f0ff 100%) !important;
            border-left: 4px solid #667eea !important;
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1) !important;
        }
        .chat-container .message[data-role="user"] {
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%) !important;
            border-left: 4px solid #0ea5e9 !important;
            box-shadow: 0 2px 8px rgba(14, 165, 233, 0.1) !important;
        }
        /* 代码块样式 */
        .chat-container pre {
            background: #f8fafc !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 6px !important;
            padding: 12px !important;
            margin: 8px 0 !important;
            overflow-x: auto !important;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace !important;
            font-size: 13px !important;
        }
        .chat-container code {
            background: #f1f5f9 !important;
            padding: 2px 4px !important;
            border-radius: 3px !important;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace !important;
            font-size: 13px !important;
            color: #475569 !important;
        }
        /* 列表样式 */
        .chat-container ul, .chat-container ol {
            margin: 8px 0 !important;
            padding-left: 20px !important;
        }
        .chat-container li {
            margin: 4px 0 !important;
            line-height: 1.5 !important;
        }
        /* 标题样式 */
        .chat-container h1, .chat-container h2, .chat-container h3 {
            color: #1e293b !important;
            margin: 12px 0 8px 0 !important;
            font-weight: 600 !important;
        }
        .chat-container h1 { font-size: 18px !important; }
        .chat-container h2 { font-size: 16px !important; }
        .chat-container h3 { font-size: 15px !important; }
        /* 强调文本 */
        .chat-container strong, .chat-container b {
            color: #1e293b !important;
            font-weight: 600 !important;
        }
        .chat-container em, .chat-container i {
            color: #475569 !important;
            font-style: italic !important;
        }
        .input-container {
            background: white;
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            margin-top: 15px;
        }
        .title-container {
             background: transparent;
             border-radius: 0;
             padding: 8px 0;
             margin: 0 auto 15px auto;
             box-shadow: none;
             text-align: center;
             max-width: 800px;
             border-bottom: 2px solid rgba(102, 126, 234, 0.2);
         }
        """

        with gr.Blocks(
            theme=gr.themes.Soft(
                primary_hue="blue",
                secondary_hue="indigo",
                neutral_hue="slate",
                font=gr.themes.GoogleFont("Inter")
            ),
            css=custom_css,
            title="AI PPT生成器"
        ) as demo:
            # 状态管理
            session_state = gr.State({})
            stored_messages = gr.State([])

            with gr.Column(elem_classes="main-container"):
                # 美化标题区域
                with gr.Row():
                    with gr.Column(elem_classes="title-container"):
                        gr.HTML("""
                        <div style="text-align: center;">
                            <div style="font-size: 2em; margin-bottom: 6px;">📊</div>
                            <h1 style="margin: 0 0 4px 0; color: #2c3e50; font-weight: 700; font-size: 1.8em; background: linear-gradient(45deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; letter-spacing: -1px;">
                                AI PPT生成器
                            </h1>
                            <p style="margin: 0; color: #7f8c8d; font-size: 0.95em; font-weight: 300;">
                                智能创建专业演示文稿
                            </p>
                        </div>
                        """)

                # 美化聊天区域
                chatbot = gr.Chatbot(
                    type="messages",
                    avatar_images=(
                        "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
                        "https://cdn-icons-png.flaticon.com/512/4712/4712109.png"
                    ),
                    height=750,
                    show_copy_button=True,
                    elem_classes="chat-container",
                    placeholder="👋 您好！我是AI助手，请告诉我您想要创建什么样的PPT..."
                )

                # 美化输入区域
                with gr.Row(elem_classes="input-container"):
                    with gr.Column():
                        with gr.Row():
                            text_input = gr.Textbox(
                                lines=2,
                                placeholder="💡 请输入您的PPT主题或详细需求...\n例如：制作一个关于人工智能发展的演示文稿",
                                container=False,
                                scale=4,
                                show_label=False
                            )
                            with gr.Column(scale=1, min_width=120):
                                submit_btn = gr.Button(
                                    "🚀 生成PPT", 
                                    variant="primary",
                                    size="lg"
                                )
                                clear_btn = gr.Button(
                                    "🗑️ 清空对话",
                                    variant="secondary"
                                )

            # 事件处理
            # 提交事件
            def submit_and_interact(text_input, messages, session_state):
                if not text_input.strip():
                    raise gr.Error("请输入内容后再提交")
                
                # 记录用户消息
                message = text_input
                
                # 与agent交互
                for updated_messages in self.interact_with_agent(message, messages, session_state):
                    yield updated_messages, "", gr.Button(interactive=False)
                
                # 重新启用按钮
                yield updated_messages, "", gr.Button(interactive=True)

            text_input.submit(
                submit_and_interact,
                [text_input, stored_messages, session_state],
                [chatbot, text_input, submit_btn]
            )

            submit_btn.click(
                submit_and_interact,
                [text_input, stored_messages, session_state],
                [chatbot, text_input, submit_btn]
            )

            # 清空按钮
            clear_btn.click(
                lambda: ([], [], ""),
                outputs=[chatbot, stored_messages, text_input]
            )

        return demo

    def launch(self, share: bool = True, **kwargs):
        """启动Gradio应用"""
        self.create_app().launch(
            debug=True, 
            share=share, 
            server_name="0.0.0.0",
            server_port=7862,
            **kwargs
        )


def main():
    """主函数"""
    # 初始化监控
    register()
    SmolagentsInstrumentor().instrument()
    
    # 创建并启动UI
    ui = PPTGeneratorUI(
        agent=ppt_generate_agent,
        reset_agent_memory=False
    )
    ui.launch(share=True)


if __name__ == "__main__":
    main()