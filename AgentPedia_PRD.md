AI Agent 信息聚合平台 PRD 文档
一、产品概述
1.1 产品名称
AgentPedia
1.2 产品定位
全球首个专注于 AI Agent 领域的信息聚合平台，为 AI Agent 开发者、研究者、投资者提供全面、实时的行业信息查询服务，助力用户快速了解全球 AI Agent 生态动态。
1.3 核心价值
- 打破信息壁垒：整合全球 AI Agent 项目信息，解决分散化查询痛点
- 助力技术交流：为开发者提供技术栈参考、功能对比的便捷渠道
- 赋能行业研究：通过结构化数据呈现 AI Agent 行业发展趋势
1.4 商业模式
AgentPedia致力于为全球AI Agent生态提供完全免费的信息服务。在当前阶段，平台所有功能和服务均免费开放，不设置任何付费门槛，专注于产品价值和用户体验的提升。

未来发展方向：
- 潜在盈利模式：API服务、高级功能、合作伙伴关系等
- 核心承诺：在可预见的未来，平台核心功能将始终保持免费
- 发展理念：通过免费优质服务建立行业影响力，为AI Agent生态发展贡献价值
二、目标用户
1. AI Agent 开发者：需参考同类产品技术方案、功能设计的工程师及团队
2. 行业研究者：关注 AI Agent 技术演进与应用场景的分析师、学者
3. 投资者：需了解项目融资情况、市场潜力的投资机构及个人
4. 技术爱好者：对 AI Agent 领域感兴趣的普通用户
三、核心功能需求
3.1 AI Agent 列表功能
3.1.1 基础展示
- 以卡片式布局展示全球 AI Agent 项目列表
- 每张卡片包含核心信息：项目名称、logo、一句话功能简介、开发状态（上线/测试/概念）
- 支持列表/网格两种视图切换
3.1.2 筛选与分类
- 按技术领域分类（如办公自动化、代码生成、生活服务等）
- 按开发阶段筛选（概念期/测试期/正式发布）
- 按上线时间排序（最新/最热）
- 按技术栈筛选（如基于 LLM 类型、框架等）
3.1.3 搜索功能
- 支持项目名称、功能关键词、技术栈等多维度搜索
- 搜索结果实时展示，支持联想提示
3.2 AI Agent 详情功能
3.2.1 基础信息模块
- 项目名称、官方 logo、官网链接（支持跳转）
- 开发团队信息（团队名称、所在地、核心成员背景）
- 项目简介（一句话概括）、详细功能说明（分点描述）
- 开发状态与上线时间
3.2.2 技术信息模块
- 核心技术栈（如基础模型、开发框架、部署方式）
- 技术特点与创新点（文本描述+标签展示）
- 开源情况（是否开源、代码仓库链接）
- 接口开放情况（API 文档链接、调用方式简介）
3.2.3 商业信息模块
- 融资情况（融资轮次、金额、投资方，历史融资记录）
- 商业模式（免费/订阅/付费 API 等）
- 用户规模（公开数据：注册用户数、日活等）
- 合作与生态（合作伙伴、集成场景）
3.2.4 附加功能
- 相关项目推荐（基于技术领域、功能相似性）
- 信息更新时间戳（明确数据时效性）
- 收藏功能（登录用户可收藏项目）

3.3 平台商业模式说明
3.3.1 免费服务策略
- 所有核心功能完全免费：Agent信息查询、搜索、详情查看、收藏等
- 无注册门槛：游客用户可访问所有信息，注册用户享受个性化功能
- 无广告干扰：专注于纯净的信息服务体验
- 无数据限制：不限制查询次数、访问频率

3.3.2 价值创造理念
- 通过免费优质服务建立行业权威性和用户信任
- 为AI Agent生态发展提供基础设施支持
- 促进行业信息透明化，降低技术交流门槛
- 建立全球AI Agent领域的信息标准和规范

3.3.3 可持续发展考虑
- 当前阶段：专注产品价值和用户体验，不考虑盈利
- 未来可能性：在保持核心功能免费的前提下，探索增值服务
- 潜在方向：企业级API服务、深度分析报告、定制化数据服务
- 原则承诺：核心信息查询功能将始终保持免费开放
四、非功能需求
4.1 性能要求
- 页面加载时间≤2秒（全球主要地区）
- 支持日均10万级访问量
- 搜索响应时间≤500ms
4.2 数据质量
- 信息准确率≥95%（核心字段）
- 重要项目信息更新频率≤7天
- 支持用户反馈数据错误（纠错通道）
4.3 兼容性
- 适配主流浏览器（Chrome、Safari、Firefox等）
- 支持移动端响应式布局（手机、平板）
4.4 安全性
- 用户数据加密存储（收藏、账号信息）
- 防爬虫机制（保护数据原创性）
- 合规性：符合GDPR等全球数据隐私法规
五、页面结构
1. 首页
  - 顶部导航栏（搜索框、分类入口、登录 / 注册）
  - 热门 AI Agent 推荐区（基于访问量）
  - 最新上线项目区
  - 行业动态简讯（可选）
2. 列表页
  - 左侧筛选栏（分类、技术栈、时间等）
  - 右侧项目展示区（支持视图切换）
  - 分页 / 无限滚动加载
3. 详情页
  - 顶部：项目名称、logo、官网链接、收藏按钮
  - 中部：分标签页展示基础信息、技术信息、商业信息
  - 底部：相关推荐、数据反馈入口
4. 个人中心（简化版）
  - 我的收藏列表
  - 浏览历史
  - 账号设置
5. 微信扫码登录页面
  - 页面标题与说明文字
  - 微信二维码展示区域（含有效期提示）
  - 扫码状态提示动画 / 文字
  - 操作按钮（刷新二维码、返回首页）
  - 底部版权信息
  - 说明：平台仅支持微信扫码登录，确保用户身份安全性
6. 管理员后台页面
  - 左侧导航菜单（信息管理、审核中心、系统设置等）
  - 顶部：搜索框、通知中心、管理员信息、退出登录
  - Agent 列表管理页：
    - 数据筛选与搜索区
    - 项目列表（支持分页）
    - 操作按钮区（新增、批量操作）
  - Agent 编辑 / 新增页：
    - 多标签页表单（基础信息、技术信息、商业信息）
    - 预览功能
    - 保存 / 提交按钮
  - 审核管理页：
    - 待审核列表
    - 审核操作区（通过 / 拒绝 + 理由）
    - 审核历史查询
  - 系统统计页：
    - 数据可视化图表
    - 关键指标展示
    - 导出功能
六、前端实现方案
6.1、技术栈概述
基于需求采用轻量高效且适配科技感风格的技术组合，确保跨端兼容性与性能：
- 核心框架：React 18 + Next.js 14（App Router）- 支持服务端渲染（SSR）与静态生成（SSG），优化首屏加载与SEO
- 样式解决方案：Tailwind CSS v3 - 实现灵活的主题切换与响应式设计，降低样式维护成本
- 状态管理：React Context（主题/国际化状态）+ SWR（数据缓存与实时更新）- 轻量且贴合Next.js生态
- 国际化：next-intl - 支持中英双语无缝切换，适配全球开发者用户
- UI增强：Headless UI（无样式组件骨架）+ Framer Motion（动画效果）- 保障交互体验与科技感视觉呈现
- 图标系统：Font Awesome + 自定义科技感线性图标 - 统一视觉语言
6.2、项目结构设计
/
├── app/                      # Next.js 14 App Router核心目录
│   ├── [locale]/             # 国际化路由（en/zh）
│   │   ├── page.tsx          # 首页
│   │   ├── agents/           # AI Agent列表页
│   │   ├── agents/[id]/      # AI Agent详情页
│   │   ├── login/            # 微信扫码登录页
│   │   ├── dashboard/        # 用户个人中心（收藏/浏览历史）
│   │   └── admin/            # 管理员后台
│   │       ├── agents/       # Agent信息增删改查
│   │       ├── review/       # 信息审核（用户提交/爬虫数据）
│   │       └── stats/        # 数据统计（访问量/项目数）
│   ├── api/                  # 后端接口代理（避免跨域）
│   ├── layout.tsx            # 根布局（注入主题/国际化上下文）
│   └── globals.css           # 全局样式（Tailwind基础配置）
├── components/               # 组件库（按功能模块化）
│   ├── ui/                   # 基础UI组件（按钮/输入框/卡片等）
│   ├── layout/               # 布局组件（导航栏/页脚/侧边栏）
│   ├── agents/               # Agent业务组件（列表项/详情面板）
│   ├── admin/                # 管理员专用组件（表单/审核列表）
│   ├── auth/                 # 认证组件（微信扫码面板/状态提示）
│   └── features/             # 功能组件（主题切换/语言选择器）
├── lib/                      # 工具库
│   ├── hooks/                # 自定义钩子（主题切换/数据请求）
│   ├── utils/                # 工具函数（日期格式化/数据校验）
│   ├── services/             # API服务（统一请求封装）
│   └── store/                # 状态管理（主题/用户状态上下文）
├── public/                   # 静态资源
│   ├── logos/                # 平台Logo与科技感装饰元素
│   ├── icons/                # 自定义科技感图标
│   └── illustrations/        # 科技风插图（首页Hero区/空状态）
├── locales/                  # 国际化翻译文件（en.json/zh.json）
└── config/                   # 配置文件（主题色值/路由映射）

6.3、设计系统（重点：亮黑Dark Mode适配）
3.1 配色方案（科技感风格）
核心原则
- 亮黑为主色调，搭配低饱和度黑色/纯黑作为辅助色，避免纯黑的沉闷感
- 明暗对比强烈，确保文本可读性与交互元素辨识度
- 支持主题无缝切换，Light Mode与Dark Mode色值一一对应
具体色值定义
颜色类型
Light Mode（浅色模式）
Dark Mode（亮黑模式）
用途说明
主色调
#FFFFFF（纯白）
#111111（亮黑，带细微光泽感）
页面背景、卡片底色
主色辅助
#F5F7FA（浅灰）
#1E1E1E（深灰，亮黑衍生色）
次级背景（侧边栏/表单区域）
强调色1（黑色）
#000000
#000000（纯黑，带发光质感）
按钮、链接、重点文本
强调色2（黑色）
#000000
#000000（纯黑，高对比度）
标签、徽章、进度条
强调色3（黑色）
#000000
#000000（纯黑，科技感辅助）
状态提示（成功/在线）、图标
文本主色
#1D2129（近黑）
#E5E7EB（近白）
正文、标题
文本次级
#4E5969（深灰）
#8A8F98（浅灰）
辅助说明、占位文本
边框/分割线
#E5E6EB（中灰）
#2D2D2D（深灰）
卡片边框、区域分割
交互反馈色
#FF4D4F（红色）
#000000（纯黑）
错误提示、删除按钮
发光效果色
rgba(0,0,0,0.1)
rgba(0,0,0,0.2)
按钮hover、输入框聚焦、卡片悬浮

3.2 排版系统（科技感无衬线风格）
- 字体选择：Inter（无衬线字体，清晰锐利，适配代码与正文）
- 字体层级：
文本类型
Light Mode/Dark Mode样式
适用场景
H1（大标题）
4xl/5xl（响应式），字重700
首页Hero区、页面顶部标题
H2（小标题）
3xl/4xl，字重600
模块标题（列表区/详情区）
H3（子标题）
2xl/3xl，字重600
卡片标题、表单分区标题
正文大
lg，字重400，行高1.5
详情描述、说明文本
正文默认
base，字重400，行高1.5
列表项描述、普通文本
正文小
sm，字重400，行高1.4
辅助说明、时间戳、标签
代码/数据
sm，字重500，等宽字体（JetBrains Mono）
技术栈展示、版本号
3.3 组件设计规范（科技感视觉强化）
通用组件
- 卡片：
  - Light Mode：纯白背景，1px浅灰边框，轻微阴影（0 2px 8px rgba(0,0,0,0.05)）
  - Dark Mode：亮黑（#111111）背景，1px深灰（#2D2D2D）边框，内发光效果（hover时边框变为黑色发光）
  - 圆角：8px（统一圆角，避免尖锐感）
- 按钮：
  - 主按钮：黑色/纯黑背景，hover时轻微缩放（1.02倍）+ 边缘发光（1px同色系发光）
  - 次按钮：透明背景，边框式设计，hover时背景变为对应色的10%透明度
  - 尺寸：默认（h-10 px-4）、小（h-8 px-3）、大（h-12 px-6）
- 输入框：
  - Light Mode：纯白背景，浅灰边框，聚焦时边框变为黑色+发光效果
  - Dark Mode：亮黑衍生色（#1E1E1E）背景，深灰边框，聚焦时边框变为纯黑+发光效果
  - 内置图标：搜索/清除图标，颜色与文本次级色一致
特色组件（科技感强化）
- 主题切换按钮：
  - Light Mode：月亮图标（深灰色），点击切换为Dark Mode（亮黑背景+黑色月亮图标）
  - Dark Mode：太阳图标（纯黑色），点击切换为Light Mode（纯白背景+深灰太阳图标）
  - 过渡动画：0.3s平滑色值过渡，图标旋转180°
- 语言切换器：
  - 下拉式设计，选中语言旁加黑色小圆点标识
  - 展开时带轻微渐入动画，选项hover时背景变为对应主题的次级色
- Agent列表项：
  - 左侧Logo区域带轻微发光边框（Dark Mode更明显）
  - 右侧功能标签（如"开源""热门"）用科技感色彩（纯黑），圆角4px
  - hover时整体上移2px，阴影加深（Light Mode）/发光增强（Dark Mode）
6.4 核心功能实现方案
4.1 主题切换（Light/Dark Mode）
实现逻辑
1. 状态存储：通过React Context管理主题状态，初始值优先读取localStorage（用户上次选择），无则适配系统主题（window.matchMedia('(prefers-color-scheme: dark)')）
2. 切换触发：导航栏主题按钮点击时，切换主题状态，并同步更新localStorage
3. 样式适配：基于Tailwind的dark:前缀，所有组件样式均编写Light/Dark双版本，例如：
  - 页面背景：bg-white dark:bg-[#111111]
  - 文本颜色：text-[#1D2129] dark:text-[#E5E7EB]
  - 边框颜色：border-[#E5E6EB] dark:border-[#2D2D2D]
4. 过渡效果：全局添加主题切换过渡（transition-colors duration-300），避免颜色突变的生硬感
关键体验点
- Dark Mode下所有发光效果（按钮hover、输入框聚焦）强度高于Light Mode，增强科技感
- 图片资源适配：部分插图提供Light/Dark两个版本，根据主题自动切换（如首页Hero区背景图）
4.2 中英文切换（国际化）
实现逻辑
5. 路由设计：采用Next.js动态路由[locale]，支持/en（英文）/zh（中文）前缀，默认路由跳转时保留当前语言
6. 翻译文件：locales目录下维护en.json与zh.json，按页面/组件模块化组织翻译文本，例如：
  - 首页Hero标题：en→"AgentPedia - The Global AI Agent Explorer"，zh→"AgentPedia - 全球AI Agent探索平台"
  - Agent详情标签：en→"Tech Stack"，zh→"技术栈"
7. 切换触发：导航栏语言选择器，点击切换时跳转至对应语言路由（如从/zh/agents跳至/en/agents），并保留当前页面位置
8. 组件适配：通过useTranslations钩子获取当前语言文本，所有静态文本均从翻译文件读取，避免硬编码
关键体验点
- 语言切换后页面不刷新（基于Next.js客户端路由），仅更新文本内容
- 表单占位符、按钮文本、提示信息等细节均实现双语适配，无遗漏
4.3 核心页面实现（Dark Mode亮黑风格适配）
1. 首页
- Hero区：
  - Light Mode：纯白背景+黑色渐变装饰（radial-gradient）
  - Dark Mode：亮黑背景+黑色渐变装饰（radial-gradient，强度更高）
  - 标题：渐变色文本（Light→黑→黑；Dark→纯黑→纯黑），带轻微发光效果
  - 搜索框：Light→纯白背景；Dark→亮黑衍生色（#1E1E1E）背景，聚焦时黑色发光
- 热门Agent推荐区：
  - 卡片布局：Light→纯白卡片；Dark→亮黑卡片，hover时黑色边框发光
  - 标签：热门标签（Trending）用亮红（Light）/纯黑（Dark），增强辨识度
- 最新上线区：
  - 时间戳：Light→深灰色；Dark→浅灰色，与卡片背景形成对比
2. AI Agent列表页
- 筛选栏：
  - Light→浅灰背景；Dark→亮黑衍生色（#1E1E1E）背景
  - 筛选选项：未选中→文本次级色；选中→黑色（Light）/纯黑（Dark）+ 底部下划线
- 列表视图：
  - 网格/列表切换：图标颜色随主题适配，选中状态用强调色
  - 加载状态：科技感骨架屏（Light→灰色占位；Dark→深灰占位，带渐变动画）
3. AI Agent详情页
- 顶部信息栏：
  - Logo区域：Light→白色背景；Dark→亮黑背景，带1px黑色边框（科技感强化）
  - 官网链接：带外部跳转图标，颜色为强调色，hover时下划线
- 标签页（基础信息/技术栈/融资情况）：
  - 未选中标签：文本次级色；选中标签：强调色+底部2px强调色边框
  - 内容区：Light→纯白背景；Dark→亮黑背景，文本清晰可读
- 相关推荐区：
  - 卡片间距增大，Dark Mode下卡片间用深灰分割线，避免视觉混淆
4. 微信扫码登录页
- 页面布局：
  - 居中卡片：Light→纯白卡片；Dark→亮黑卡片，带黑色边框（增强科技感）
  - 二维码区域：背景为主题对应色（Light→浅灰；Dark→深灰），避免二维码与背景融合
- 状态提示：
  - 未扫码：文本次级色；扫码待确认：黑色（Light）/纯黑（Dark）；登录成功：青绿；登录失败：红色
  - 刷新二维码按钮：图标+文本组合，hover时强调色高亮
5. 管理员后台
- 侧边栏：
  - Light→浅灰背景；Dark→亮黑衍生色（#1E1E1E）背景
  - 选中菜单：左侧2px强调色边框+文本强调色，背景为对应色10%透明度
- 表单区域（增删改Agent）：
  - 输入框/下拉框：Light→纯白；Dark→亮黑衍生色，聚焦时黑色发光
  - 提交/删除按钮：提交→黑色/纯黑；删除→红色，hover时发光效果
- 数据统计页：
  - 图表背景：Light→纯白；Dark→亮黑，图表线条/柱状图颜色用强调色（黑色/纯黑/纯黑）
  - 数据卡片：Light→纯白；Dark→亮黑，数值用大字号+强调色，增强视觉冲击
6.5 性能与兼容性优化
6.5.1 性能优化
9. 资源加载：
  - 静态资源（图片/图标）采用Next.js的Image组件，自动压缩+懒加载
  - 国际化翻译文件按页面拆分，避免一次性加载所有语言文本
10. 数据处理：
  - 列表数据采用SWR缓存，页面切换时不重复请求，支持后台刷新
  - 管理员后台批量操作（如批量删除）采用节流处理，避免频繁接口调用
11. 样式优化：
  - Tailwind CSS PurgeCSS按需打包，减少样式文件体积
  - 主题色值通过Tailwind配置统一管理，避免重复定义
6.5.2 兼容性适配
12. 浏览器兼容：
  - 适配Chrome、Safari、Firefox、Edge主流版本，Dark Mode在各浏览器下色值统一
  - 针对Safari的特殊样式（如input聚焦发光）单独适配，确保体验一致
13. 设备适配：
  - 响应式设计，支持桌面端（≥1200px）、平板（768px-1199px）、移动端（<768px）
  - 移动端Dark Mode下优化触摸区域（按钮尺寸≥44px×44px），避免误触
6.6 logo
请设计一款适配**AI Agent领域专业知识库（AgentPedia）** 的品牌logo，核心需贴合平台定位与视觉调性，具体需求如下：
6.6.1 品牌核心定位明确
AgentPedia是聚焦“AI智能体（Agent）”领域的垂直知识库/百科平台，核心功能为整合AI Agent技术原理、应用案例、开发工具、行业理论等内容，服务开发者、企业决策者、AI研究者三类核心用户，需通过logo传递“专业、前沿、易用”的品牌感知。
6.6.2 视觉元素方向
需融合“AI智能体”与“知识平台”两大核心符号，避免具象化、复杂设计，建议采用以下元素组合（可灵活创新）：
14. AI Agent符号：极简抽象的智能体轮廓（如线条化机器人头部、数据流构成的“Agent”首字母“A”）、低饱和度的科技感动态元素（如微缩的电路纹理、渐变光带）；
15. 知识属性符号：数字化知识载体（如线条化的“打开的百科全书”“知识图谱节点网络”“极简书架”），或用“节点连接”体现知识整合属性；
16. 整体造型：优先选择“圆形/方形/圆角矩形”等规整轮廓（确保小尺寸识别性），避免细碎装饰，核心元素占比不超过logo整体的70%，留白适度。
6.6.3 设计风格与调性
17. 主风格：极简科技风+现代简约风，贴合飞书生态的“高效、清爽”视觉基因（无需完全复刻飞书风格，保持品牌独立性）；
18. 细节要求：无多余渐变/阴影（可加极浅层次感渐变），线条流畅均匀，避免复杂纹理，确保在“飞书文档嵌入、网页图标、移动端图标、印刷物料”等场景下均能清晰识别；
19. 避免方向：拒绝卡通化、过度拟人化设计，不使用高饱和撞色，不添加与“AI Agent/知识”无关的装饰元素（如花朵、动物具象图形）。
6.6.4 色彩方案
以“专业科技感”为核心，提供2套可选配色（设计时可任选1套深化）：
- 方案1（沉稳专业款）：主色#000000（纯黑，传递信任）、辅色#000000（纯黑，体现创新）、点缀色#000000（纯黑，平衡视觉）；
- 方案2（前沿活力款）：主色#000000（纯黑）、辅色#000000（纯黑，体现智能）、点缀色#000000（纯黑，提升清爽感）；
- 配色原则：整体色彩不超过3种（主+辅+点缀），无大面积纯白/纯黑，确保在浅色（飞书文档背景）、深色（网页深色模式）背景下均能正常显示。
6.6.5 字体与排版适配
20. 文字组合：logo可包含“图形+文字”两部分（文字为“AgentPedia”英文+“AgentPedia知识库”中文，或仅“AgentPedia”英文，根据图形比例灵活调整）；
21. 字体要求：中文用无衬线字体（如思源黑体、微软雅黑，字重400-500），英文用现代无衬线字体（如Roboto、Montserrat，字重500-600），避免艺术化字体，确保远距离/小尺寸下易读；
22. 排版比例：图形与文字横向排列时，两者间距为文字高度的1/3；纵向排列时，文字在图形下方，居中对齐，整体重心稳定。
6.6.6 应用场景适配
需满足多场景缩放需求：
- 小尺寸场景（如飞书文档侧边栏图标、移动端APP图标）：核心图形无细节丢失，文字可简化为“AgentPedia”英文缩写（如“AP”）；
- 大尺寸场景（如网页Banner、印刷手册封面）：可适度增加图形细节（如浅纹理），但不破坏整体极简感。
6.6.7 情感传递优先级
23. 第一优先级：专业可靠（避免轻浮设计）；
24. 第二优先级：前沿科技（体现AI Agent领域属性）；
25. 第三优先级：友好易用（避免高冷、晦涩的视觉表达）。
可基于以上需求灵活创作，无需严格限制细节，重点确保“品牌辨识度”与“场景适配性”。
6.7 交付物清单
26. 设计资源：
  - 配色方案文档（含Light/Dark Mode色值、用途说明）
  - 组件设计规范（含Sketch/Figma设计稿，适配亮黑Dark Mode）
27. 代码交付：
  - 完整前端项目代码（按上述项目结构组织）
  - 环境配置文档（开发/生产环境部署步骤）
  - 组件使用文档（基础UI组件/业务组件调用示例）
28. 测试报告：
  - 浏览器兼容性测试报告（各浏览器Dark Mode适配情况）
  - 性能测试报告（首屏加载时间、资源体积分析）
7、后端实现方案
7.1 技术栈概述与选型理由
  基于项目需求和技术特性，后端采用以下技术栈组合：
技术组件
选型
核心价值
编程语言
Python 3.10+
生态丰富，AI/数据处理库支持完善，开发效率高
Web框架
FastAPI
高性能异步支持，自动生成API文档，类型提示严格，适合构建现代化API
AI框架
LangChain
连接各种AI模型和工具的中间层，简化AI Agent相关功能开发
多智能体框架
LangGraph
构建有状态多智能体系统，支持复杂工作流，适合数据采集和处理自动化
文档数据库
MongoDB
存储非结构化/半结构化的AI Agent信息，支持灵活的 schema 设计
关系数据库
MySQL 8.0
存储用户数据、权限管理、操作日志等结构化数据，保证事务一致性
API文档
Swagger UI (FastAPI内置)
自动生成交互式API文档，方便前后端协作
任务队列
Celery + Redis
处理异步任务（如数据爬取、信息更新、邮件通知）
部署工具
Docker + Docker Compose
容器化部署，保证开发环境与生产环境一致性
7.2 系统架构设计
7.2.1 整体架构图
  
┌─────────────────┐     ┌─────────────────────────────────────┐     ┌─────────────────┐
│                 │     │             后端服务层              │     │                 │
│   前端应用      │◄────┤  FastAPI + 中间件 + 业务逻辑层      │◄────┤  第三方服务集成  │
│  (Next.js)      │     │                                     │     │  (微信登录/爬虫) │
│                 │────►│  API路由 + 数据验证 + 权限控制      │────►│                 │
└─────────────────┘     └───────────────────┬─────────────────┘     └─────────────────┘
                                            │
                 ┌──────────────────────────┼──────────────────────────┐
                 │                          │                          │
        ┌────────▼─────────┐        ┌───────▼────────┐        ┌───────▼────────┐
        │  数据访问层      │        │  AI处理层      │        │  任务处理层    │
        │                  │        │                │        │                │
        │ - MongoDB 交互   │        │ - LangChain    │        │ - Celery 任务  │
        │ - MySQL 交互     │        │ - LangGraph    │        │ - 定时任务     │
        │ - 缓存管理       │        │ - 智能处理     │        │ - 异步任务     │
        └────────┬─────────┘        └────────────────┘        └────────────────┘
                 │
        ┌────────▼─────────┐
        │  数据存储层      │
        │                  │
        │ - MongoDB        │
        │ - MySQL          │
        │ - Redis (缓存)   │
        └──────────────────┘
7.2.2 核心服务模块
  1. API服务：基于FastAPI构建的RESTful API，处理前端请求
  2. 认证服务：处理微信扫码登录、会话管理、权限控制
  3. 数据采集服务：基于LangChain和LangGraph构建的智能爬虫，采集全球AI Agent信息
  4. 数据处理服务：清洗、结构化、标准化采集到的信息
  5. 内容管理服务：提供AI Agent信息的CRUD操作，支持管理员后台功能
  6. 搜索服务：提供高效的多维度搜索功能（名称、技术栈、功能等）

7.2.3 用户权限和角色管理设计

角色定义：

1. 游客用户（Guest）
   - 权限范围：
     * 浏览AI Agent列表和详情
     * 使用搜索功能
     * 查看公开统计信息
   - 限制：
     * 无法收藏Agent
     * 无法提交Agent信息
     * 无法访问个人中心
     * API调用频率限制：100次/小时

2. 注册用户（User）
   - 权限范围：
     * 继承游客用户所有权限
     * 收藏/取消收藏AI Agent
     * 查看个人收藏列表
     * 提交新的Agent信息（需审核）
     * 对Agent信息提出修改建议
     * 访问个人中心和设置
   - 限制：
     * 提交的内容需要审核
     * API调用频率限制：1000次/小时
     * 每日最多提交5个新Agent

3. 贡献者（Contributor）
   - 权限范围：
     * 继承注册用户所有权限
     * 提交的Agent信息优先审核
     * 参与Agent信息的协作编辑
     * 查看审核状态和反馈
   - 限制：
     * API调用频率限制：5000次/小时
     * 每日最多提交20个新Agent
   - 获得条件：
     * 成功提交并通过审核的Agent数量≥10个
     * 账户注册时间≥30天
     * 无违规记录

4. 审核员（Moderator）
   - 权限范围：
     * 继承贡献者所有权限
     * 审核用户提交的Agent信息
     * 编辑和修改Agent信息
     * 管理Agent状态（发布/下架/删除）
     * 查看用户提交历史和统计
     * 处理用户举报和反馈
   - 限制：
     * 无法删除其他审核员创建的内容
     * 无法修改系统配置
     * API调用频率限制：10000次/小时

5. 管理员（Admin）
   - 权限范围：
     * 继承审核员所有权限
     * 用户管理（查看、编辑、禁用用户）
     * 角色权限管理
     * 系统配置管理
     * 数据导入/导出
     * 查看系统监控和日志
     * 管理爬虫任务
   - 无限制：
     * 无API调用频率限制
     * 可以执行所有操作

6. 超级管理员（Super Admin）
   - 权限范围：
     * 继承管理员所有权限
     * 管理员账户的创建和删除
     * 系统核心配置修改
     * 数据库直接操作权限
     * 服务器和部署管理

权限控制实现：

1. 基于角色的访问控制（RBAC）
```python
# 权限装饰器
from functools import wraps
from flask import g, jsonify

def require_permission(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.current_user:
                return jsonify({"error": "Authentication required"}), 401
            
            if not g.current_user.has_permission(permission):
                return jsonify({"error": "Permission denied"}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# 使用示例
@app.route('/api/agents', methods=['POST'])
@require_permission('agent.create')
def create_agent():
    # 创建Agent的逻辑
    pass

@app.route('/api/admin/users', methods=['GET'])
@require_permission('user.manage')
def list_users():
    # 管理用户的逻辑
    pass
```

2. 权限矩阵设计
```python
PERMISSIONS = {
    'guest': [
        'agent.read',
        'search.use',
        'stats.read'
    ],
    'user': [
        'agent.read',
        'agent.submit',
        'search.use',
        'stats.read',
        'favorite.manage',
        'profile.read',
        'profile.update'
    ],
    'contributor': [
        'agent.read',
        'agent.submit',
        'agent.suggest_edit',
        'search.use',
        'stats.read',
        'favorite.manage',
        'profile.read',
        'profile.update',
        'review.read'
    ],
    'moderator': [
        'agent.read',
        'agent.create',
        'agent.update',
        'agent.delete',
        'agent.review',
        'agent.publish',
        'search.use',
        'stats.read',
        'favorite.manage',
        'profile.read',
        'profile.update',
        'review.manage',
        'user.read'
    ],
    'admin': [
        'agent.*',
        'user.read',
        'user.update',
        'user.disable',
        'role.assign',
        'system.config',
        'crawler.manage',
        'stats.admin',
        'log.read'
    ],
    'super_admin': [
        '*'  # 所有权限
    ]
}
```

3. 动态权限检查
```python
class User:
    def has_permission(self, permission):
        """检查用户是否具有指定权限"""
        if self.role == 'super_admin':
            return True
        
        user_permissions = PERMISSIONS.get(self.role, [])
        
        # 检查通配符权限
        for perm in user_permissions:
            if perm == '*':
                return True
            if perm.endswith('*') and permission.startswith(perm[:-1]):
                return True
            if perm == permission:
                return True
        
        return False
    
    def can_edit_agent(self, agent):
        """检查用户是否可以编辑特定Agent"""
        if self.has_permission('agent.update'):
            return True
        
        # 贡献者可以编辑自己提交的Agent
        if self.role == 'contributor' and agent.submitted_by == self.id:
            return True
        
        return False
```

4. API权限中间件
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_current_user(token: str = Depends(security)):
    """获取当前用户"""
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = await get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def require_role(required_role: str):
    """角色权限依赖"""
    def role_checker(current_user: User = Depends(get_current_user)):
        role_hierarchy = {
            'guest': 0,
            'user': 1,
            'contributor': 2,
            'moderator': 3,
            'admin': 4,
            'super_admin': 5
        }
        
        user_level = role_hierarchy.get(current_user.role, 0)
        required_level = role_hierarchy.get(required_role, 0)
        
        if user_level < required_level:
            raise HTTPException(
                status_code=403,
                detail=f"Role '{required_role}' or higher required"
            )
        
        return current_user
    
    return role_checker
```

5. 前端权限控制
```javascript
// 权限上下文
const PermissionContext = createContext();

export const PermissionProvider = ({ children }) => {
  const { user } = useAuth();
  
  const hasPermission = (permission) => {
    if (!user) return false;
    return user.permissions.includes(permission) || user.permissions.includes('*');
  };
  
  const hasRole = (role) => {
    if (!user) return false;
    const roleHierarchy = {
      'guest': 0,
      'user': 1,
      'contributor': 2,
      'moderator': 3,
      'admin': 4,
      'super_admin': 5
    };
    
    return roleHierarchy[user.role] >= roleHierarchy[role];
  };
  
  return (
    <PermissionContext.Provider value={{ hasPermission, hasRole }}>
      {children}
    </PermissionContext.Provider>
  );
};

// 权限组件
export const ProtectedComponent = ({ permission, role, children, fallback = null }) => {
  const { hasPermission, hasRole } = useContext(PermissionContext);
  
  if (permission && !hasPermission(permission)) {
    return fallback;
  }
  
  if (role && !hasRole(role)) {
    return fallback;
  }
  
  return children;
};

// 使用示例
<ProtectedComponent permission="agent.create">
  <Button onClick={createAgent}>创建Agent</Button>
</ProtectedComponent>

<ProtectedComponent role="moderator">
  <AdminPanel />
</ProtectedComponent>
```

6. 数据库权限模型
```sql
-- 用户表
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    openid VARCHAR(100) UNIQUE NOT NULL,
    nickname VARCHAR(100),
    avatar_url VARCHAR(500),
    role ENUM('guest', 'user', 'contributor', 'moderator', 'admin', 'super_admin') DEFAULT 'user',
    status ENUM('active', 'disabled', 'banned') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP,
    
    -- 统计字段
    submitted_agents_count INT DEFAULT 0,
    approved_agents_count INT DEFAULT 0,
    contribution_score INT DEFAULT 0
);

-- 权限表
CREATE TABLE permissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 角色权限关联表
CREATE TABLE role_permissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    role VARCHAR(50) NOT NULL,
    permission_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (permission_id) REFERENCES permissions(id),
    UNIQUE KEY unique_role_permission (role, permission_id)
);

-- 用户自定义权限表（特殊情况下的个别权限授予）
CREATE TABLE user_permissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    permission_id INT NOT NULL,
    granted_by INT NOT NULL,
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (permission_id) REFERENCES permissions(id),
    FOREIGN KEY (granted_by) REFERENCES users(id)
);

-- 操作日志表
CREATE TABLE operation_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50),
    resource_id VARCHAR(100),
    details JSON,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_user_action (user_id, action),
    INDEX idx_resource (resource_type, resource_id),
    INDEX idx_created_at (created_at)
);
```

7. 权限升级机制
```python
class UserRoleManager:
    @staticmethod
    async def check_auto_promotion(user_id: int):
        """检查用户是否符合自动升级条件"""
        user = await get_user_by_id(user_id)
        
        # 检查升级到贡献者的条件
        if user.role == 'user':
            if (user.approved_agents_count >= 10 and 
                user.account_age_days >= 30 and
                user.violation_count == 0):
                await promote_user(user_id, 'contributor')
                await send_promotion_notification(user_id, 'contributor')
    
    @staticmethod
    async def manual_promotion(admin_id: int, user_id: int, new_role: str, reason: str):
        """管理员手动升级用户角色"""
        admin = await get_user_by_id(admin_id)
        if not admin.has_permission('role.assign'):
            raise PermissionError("No permission to assign roles")
        
        await update_user_role(user_id, new_role)
        await log_role_change(admin_id, user_id, new_role, reason)
        await send_promotion_notification(user_id, new_role)
```

安全措施：

1. 会话管理
   - JWT Token有效期：30分钟
   - Refresh Token有效期：7天
   - 自动续期机制
   - 异地登录检测

2. 权限缓存
   - Redis缓存用户权限信息
   - 权限变更时立即清除缓存
   - 缓存有效期：1小时

3. 审计日志
   - 记录所有权限相关操作
   - 敏感操作需要二次确认
   - 定期权限审查

7.2.3 搜索技术方案设计

搜索引擎选择：
- 主搜索引擎：Elasticsearch 7.x
  - 支持全文搜索、多字段搜索、聚合分析
  - 提供强大的中文分词和英文分词能力
  - 支持实时索引更新和高并发查询
- 辅助存储：MongoDB
  - 存储原始Agent数据，作为搜索结果的数据源
  - 提供复杂查询和数据关联功能
- 缓存层：Redis
  - 缓存热门搜索结果和搜索建议
  - 存储用户搜索历史和个性化推荐

索引设计策略：
```json
{
  "agents_index": {
    "mappings": {
      "properties": {
        "name": {
          "type": "object",
          "properties": {
            "zh": {"type": "text", "analyzer": "ik_max_word"},
            "en": {"type": "text", "analyzer": "english"}
          }
        },
        "description": {
          "type": "object", 
          "properties": {
            "zh": {
              "type": "object",
              "properties": {
                "short": {"type": "text", "analyzer": "ik_max_word"},
                "detailed": {"type": "text", "analyzer": "ik_max_word"}
              }
            },
            "en": {
              "type": "object",
              "properties": {
                "short": {"type": "text", "analyzer": "english"},
                "detailed": {"type": "text", "analyzer": "english"}
              }
            }
          }
        },
        "features": {
          "type": "object",
          "properties": {
            "zh": {"type": "text", "analyzer": "ik_max_word"},
            "en": {"type": "text", "analyzer": "english"}
          }
        },
        "technical_stack": {
          "type": "object",
          "properties": {
            "base_model": {"type": "keyword"},
            "frameworks": {"type": "keyword"},
            "programming_languages": {"type": "keyword"}
          }
        },
        "tags": {"type": "keyword"},
        "status": {"type": "keyword"},
        "created_at": {"type": "date"},
        "updated_at": {"type": "date"},
        "popularity_score": {"type": "float"}
      }
    }
  }
}
```

搜索功能实现：
1. 多维度搜索：
   - 项目名称搜索（中英文）
   - 功能关键词搜索（支持模糊匹配）
   - 技术栈精确匹配（框架、编程语言、基础模型）
   - 标签分类搜索
   - 开发团队搜索

2. 查询构建示例：
```json
{
  "query": {
    "bool": {
      "should": [
        {
          "multi_match": {
            "query": "用户输入关键词",
            "fields": [
              "name.zh^3", "name.en^3",
              "description.zh.short^2", "description.en.short^2", 
              "description.zh.detailed", "description.en.detailed",
              "features.zh^1.5", "features.en^1.5"
            ],
            "type": "best_fields",
            "fuzziness": "AUTO"
          }
        },
        {
          "terms": {
            "technical_stack.frameworks": ["用户选择的框架"]
          }
        }
      ],
      "filter": [
        {"term": {"status": "released"}},
        {"range": {"created_at": {"gte": "用户选择的时间范围"}}}
      ]
    }
  },
  "sort": [
    {"popularity_score": {"order": "desc"}},
    {"_score": {"order": "desc"}},
    {"updated_at": {"order": "desc"}}
  ],
  "highlight": {
    "fields": {
      "name.*": {},
      "description.*.short": {},
      "features.*": {}
    }
  }
}
```

智能搜索增强：
1. 自动补全：
   - 基于历史搜索数据生成搜索建议
   - 支持拼音搜索和英文缩写
   - 实时更新热门搜索词

2. 同义词扩展：
   - 维护AI Agent领域专业术语同义词库
   - 支持中英文术语互译搜索
   - 自动扩展相关技术栈搜索

3. 拼写纠错：
   - 英文单词拼写检查和建议
   - 中文输入法错误纠正
   - 搜索结果"您是否要找"提示

4. 智能排序算法：
   - 综合相关性评分、热度评分、时效性评分
   - 个性化推荐（基于用户搜索历史）
   - A/B测试优化排序策略

性能优化策略：
1. 索引优化：
   - 定期重建索引，优化查询性能
   - 使用索引模板，统一索引配置
   - 监控索引大小和查询延迟

2. 缓存策略：
   - 热门搜索结果缓存（TTL: 10分钟）
   - 搜索建议缓存（TTL: 1小时）
   - 用户个性化搜索缓存（TTL: 30分钟）

3. 查询优化：
   - 使用filter查询减少评分计算
   - 限制搜索结果数量（默认20条，最大100条）
   - 异步预加载热门搜索结果

数据同步机制：
1. 实时同步：
   - MongoDB数据变更触发Elasticsearch索引更新
   - 使用Change Streams监听数据变化
   - 确保搜索结果的实时性

2. 批量同步：
   - 定时全量同步（每日凌晨）
   - 增量同步（每小时）
   - 数据一致性校验和修复

搜索分析与监控：
- 搜索关键词统计和分析
- 搜索结果点击率监控
- 搜索性能指标监控（响应时间、QPS）
- 用户搜索行为分析和优化建议
  7. 通知服务：处理系统通知、审核提醒等
7.3 数据模型设计

7.3.0 多语言Agent信息管理方案

数据存储策略：
- Agent名称、描述、功能特点、技术栈、团队信息等关键字段支持中英文双语版本
- 采用嵌套JSON结构存储多语言内容，便于扩展和维护
- 数据结构示例：
```json
{
  "name": {
    "zh": "AutoGPT自主智能体",
    "en": "AutoGPT Autonomous Agent"
  },
  "description": {
    "zh": {
      "short": "开源自主AI智能体",
      "detailed": "AutoGPT是一个实验性的开源项目，旨在让GPT-4完全自主运行..."
    },
    "en": {
      "short": "Open-source autonomous AI agent", 
      "detailed": "AutoGPT is an experimental open-source attempt to make GPT-4 fully autonomous..."
    }
  },
  "features": {
    "zh": ["自主任务规划", "内存管理", "互联网访问"],
    "en": ["Autonomous task planning", "Memory management", "Internet access"]
  },
  "technical_stack": {
    "zh": {
      "base_model": ["GPT-4", "GPT-3.5"],
      "frameworks": ["LangChain"],
      "description": "基于大语言模型的自主智能体框架"
    },
    "en": {
      "base_model": ["GPT-4", "GPT-3.5"],
      "frameworks": ["LangChain"], 
      "description": "Autonomous agent framework based on large language models"
    }
  },
  "development_team": {
    "zh": {
      "name": "SigGravitas团队",
      "location": "全球",
      "description": "专注于AI自主智能体研发的开源团队"
    },
    "en": {
      "name": "SigGravitas",
      "location": "Global",
      "description": "Open-source team focused on AI autonomous agent development"
    }
  }
}
```

内容管理流程：
1. 爬虫采集：优先采集英文原始信息，AI翻译生成中文版本
2. 人工审核：管理员审核AI翻译质量，必要时进行人工校正
3. 用户贡献：用户可提交中英文信息补充，经审核后更新
4. 术语库：维护AI Agent领域专业术语中英文对照表，确保翻译一致性
5. 内容更新：当英文原始信息更新时，自动触发中文翻译更新流程

API设计：
- 支持按语言查询：GET /api/v1/agents?lang=zh|en
- 增强搜索：支持中英文混合关键词搜索，优先返回对应语言结果
- 管理员API：支持批量翻译、内容审核、术语管理

前端展示策略：
- 语言切换：根据用户选择的语言显示对应版本内容
- URL路径：/zh/agents/[id] 和 /en/agents/[id] 分别显示中英文版本
- 内容优化：当某语言版本内容缺失时，显示另一语言版本并标注
- SEO优化：为中英文页面分别生成meta标签和结构化数据

质量保障：
- 翻译质量控制：AI翻译+人工审核双重保障
- 内容同步：确保中英文版本信息的一致性和时效性
- 用户反馈：提供翻译质量反馈机制，持续优化翻译效果

7.3.1 MongoDB 文档模型（主要存储AI Agent信息）
  
AI Agent 核心信息集合（agents）
{
  "_id": "ObjectId()",
  "name": "AutoGPT",  // 名称
  "slug": "auto-gpt",  // URL友好名称
  "logo_url": "https://example.com/logos/autogpt.png",  // Logo地址
  "official_url": "https://autogpt.net",  // 官网地址
  "description": {
    "short": "开源自主AI代理",  // 短描述
    "detailed": "AutoGPT是一个实验性开源项目，旨在使GPT-4完全自主...",  // 详细描述
    "en": {
      "short": "Open-source autonomous AI agent",
      "detailed": "AutoGPT is an experimental open-source attempt to make GPT-4 fully autonomous..."
    }
  },
  "development_team": {
    "name": "SigGravitas",  // 团队名称
    "location": "Global",  // 所在地
    "members": ["Toran Bruce Richards"],  // 核心成员
    "website": "https://siggravitas.com"  // 团队官网
  },
  "technical_stack": {
    "base_model": ["GPT-4", "GPT-3.5"],  // 基础模型
    "frameworks": ["LangChain"],  // 框架
    "programming_languages": ["Python"],  // 编程语言
    "deployment": ["Docker", "Cloud"]  // 部署方式
  },
  "features": [
    "自主任务规划", "内存管理", "互联网访问"  // 功能特点
  ],
  "business_info": {
    "funding": [
      {
        "round": "种子轮",
        "amount": "未披露",
        "investors": ["不详"],
        "date": "2023-04"
      }
    ],
    "business_model": "开源免费",  // 商业模式
    "user_scale": {
      "registered_users": "10万+",  // 注册用户数
      "active_users": "5万+",  // 活跃用户数
      "source": "第三方统计",  // 数据来源
      "updated_at": "2025-03-15"  // 数据更新时间
    }
  },
  "status": "released",  // 状态：concept/alpha/beta/released
  "tags": ["autonomous", "open-source", "general"],  // 标签
  "related_agents": ["ObjectId()", "ObjectId()"],  // 相关Agent
  "metrics": {
    "stars": 150000,  // GitHub星数
    "forks": 20000,  // GitHub分叉数
    "contributors": 1000  // 贡献者数量
  },
  "timeline": [
    {
      "event": "首次发布",
      "date": "2023-03-15"
    }
  ],
  "created_at": "2025-01-10T08:30:00Z",  // 创建时间
  "updated_at": "2025-04-20T15:45:00Z",  // 更新时间
  "last_scraped_at": "2025-04-19T02:15:00Z",  // 最后爬取时间
  "created_by": "system",  // 创建者：system/admin/user_id
  "is_verified": true  // 是否经过验证
}
  
其他MongoDB集合
  - agent_categories：AI Agent分类信息
  - scraping_sources：数据采集来源配置
  - system_configs：系统配置信息
7.3.2 MySQL 关系模型（主要存储结构化数据）
  
用户表（users）
CREATE TABLE users (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  openid VARCHAR(100) UNIQUE NOT NULL COMMENT '微信OpenID',
  nickname VARCHAR(50) COMMENT '用户昵称',
  avatar_url VARCHAR(255) COMMENT '头像URL',
  email VARCHAR(100) UNIQUE COMMENT '邮箱',
  role ENUM('user', 'admin', 'super_admin') DEFAULT 'user' COMMENT '角色',
  status ENUM('active', 'inactive', 'banned') DEFAULT 'active' COMMENT '状态',
  last_login_at DATETIME COMMENT '最后登录时间',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
  
收藏表（user_favorites）
CREATE TABLE user_favorites (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT NOT NULL COMMENT '用户ID',
  agent_id VARCHAR(50) NOT NULL COMMENT 'Agent ID(MongoDB ObjectId)',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uk_user_agent (user_id, agent_id),
  KEY idx_user_id (user_id)
);
  
操作日志表（operation_logs）
CREATE TABLE operation_logs (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT COMMENT '操作用户ID',
  operation_type ENUM('create', 'update', 'delete', 'login', 'logout', 'verify') NOT NULL COMMENT '操作类型',
  resource_type ENUM('agent', 'user', 'category', 'system') NOT NULL COMMENT '资源类型',
  resource_id VARCHAR(100) COMMENT '资源ID',
  details JSON COMMENT '操作详情',
  ip_address VARCHAR(50) COMMENT 'IP地址',
  user_agent TEXT COMMENT '用户代理',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY idx_user_id (user_id),
  KEY idx_created_at (created_at)
);
  
其他MySQL表
  - user_sessions：用户会话管理
  - admin_permissions：管理员权限
  - audit_records：内容审核记录

7.3.3 数据验证规则和约束设计

Agent信息字段验证规则：

1. 基础信息验证：
```python
{
  "name": {
    "type": "string",
    "min_length": 1,
    "max_length": 100,
    "pattern": "^[a-zA-Z0-9\\s\\-_\\.]+$",
    "required": True,
    "description": "项目名称，支持英文、数字、空格、连字符、下划线、点号"
  },
  "slug": {
    "type": "string", 
    "min_length": 1,
    "max_length": 50,
    "pattern": "^[a-z0-9\\-]+$",
    "required": True,
    "unique": True,
    "description": "URL友好名称，仅支持小写字母、数字、连字符"
  },
  "logo_url": {
    "type": "url",
    "max_length": 500,
    "allowed_domains": ["*.amazonaws.com", "*.cloudfront.net", "*.github.com"],
    "file_types": ["jpg", "jpeg", "png", "svg", "webp"],
    "max_file_size": "2MB",
    "required": False
  },
  "official_url": {
    "type": "url",
    "max_length": 500,
    "required": True,
    "must_be_accessible": True,
    "description": "官网地址必须可访问"
  }
}
```

2. 描述信息验证：
```python
{
  "description.short": {
    "type": "string",
    "min_length": 10,
    "max_length": 200,
    "required": True,
    "description": "简短描述，10-200字符"
  },
  "description.detailed": {
    "type": "string",
    "min_length": 50,
    "max_length": 2000,
    "required": True,
    "description": "详细描述，50-2000字符"
  },
  "description.en.short": {
    "type": "string",
    "min_length": 10,
    "max_length": 300,
    "pattern": "^[a-zA-Z0-9\\s\\.,!?\\-_()]+$",
    "required": False,
    "description": "英文简短描述"
  }
}
```

3. 技术栈验证：
```python
{
  "technical_stack.base_model": {
    "type": "array",
    "items": {
      "type": "string",
      "enum": ["GPT-4", "GPT-3.5", "Claude", "Gemini", "LLaMA", "PaLM", "其他"]
    },
    "max_items": 5,
    "required": True
  },
  "technical_stack.frameworks": {
    "type": "array", 
    "items": {
      "type": "string",
      "enum": ["LangChain", "LangGraph", "AutoGen", "CrewAI", "Semantic Kernel", "其他"]
    },
    "max_items": 10,
    "required": False
  },
  "technical_stack.programming_languages": {
    "type": "array",
    "items": {
      "type": "string", 
      "enum": ["Python", "JavaScript", "TypeScript", "Java", "Go", "Rust", "C++", "其他"]
    },
    "max_items": 5,
    "required": False
  }
}
```

4. 商业信息验证：
```python
{
  "business_info.funding": {
    "type": "array",
    "items": {
      "type": "object",
      "properties": {
        "round": {
          "type": "string",
          "enum": ["种子轮", "天使轮", "Pre-A", "A轮", "B轮", "C轮", "D轮", "战略投资", "IPO", "未披露"]
        },
        "amount": {
          "type": "string",
          "max_length": 50,
          "pattern": "^[0-9\\.]+[万千亿]?[美元人民币]?$|^未披露$"
        },
        "date": {
          "type": "string",
          "format": "YYYY-MM",
          "min_date": "2020-01",
          "max_date": "current_month"
        }
      }
    },
    "max_items": 10
  },
  "business_info.user_scale.registered_users": {
    "type": "string",
    "pattern": "^[0-9]+[万千亿]?\\+?$|^未披露$",
    "description": "用户规模格式：数字+单位+可选加号，如'10万+'或'未披露'"
  }
}
```

5. 状态和标签验证：
```python
{
  "status": {
    "type": "string",
    "enum": ["concept", "alpha", "beta", "released", "discontinued"],
    "required": True,
    "description": "项目状态必须为预定义值之一"
  },
  "tags": {
    "type": "array",
    "items": {
      "type": "string",
      "min_length": 2,
      "max_length": 20,
      "pattern": "^[a-zA-Z0-9\\u4e00-\\u9fa5\\-_]+$"
    },
    "min_items": 1,
    "max_items": 10,
    "unique_items": True,
    "description": "标签数组，1-10个，每个标签2-20字符"
  }
}
```

业务规则约束：

1. 唯一性约束：
   - Agent名称在同一语言下不能重复
   - slug全局唯一
   - 官网URL不能重复（同一项目的不同版本除外）

2. 关联性约束：
   - related_agents中的ID必须存在于agents集合中
   - user_favorites中的agent_id必须存在
   - 用户不能重复收藏同一个Agent

3. 时间约束：
   - created_at不能晚于updated_at
   - 融资时间不能早于2020年
   - last_scraped_at不能晚于当前时间

4. 内容质量约束：
   - 描述不能包含敏感词汇
   - URL必须是有效且可访问的
   - 图片URL必须返回有效的图片文件

安全过滤规则：

1. XSS防护：
   - 所有用户输入进行HTML转义
   - 富文本内容使用白名单标签过滤
   - URL参数进行编码处理

2. SQL注入防护：
   - 使用参数化查询
   - 输入长度限制
   - 特殊字符转义

3. 文件上传安全：
   - 文件类型白名单验证
   - 文件大小限制
   - 文件内容扫描（防病毒）
   - 文件名安全检查

4. 输入清洗：
```python
def sanitize_input(data):
    """输入数据清洗函数"""
    # 移除前后空格
    if isinstance(data, str):
        data = data.strip()
    
    # HTML标签清理
    data = bleach.clean(data, tags=[], strip=True)
    
    # 特殊字符过滤
    data = re.sub(r'[<>"\']', '', data)
    
    return data
```

数据完整性检查：

1. 定期数据一致性检查：
   - 检查related_agents引用的有效性
   - 验证URL的可访问性
   - 检查图片链接的有效性

2. 数据质量评分：
   - 必填字段完整性：40%
   - 描述内容质量：30%
   - 技术信息完整性：20%
   - 商业信息完整性：10%

3. 自动修复机制：
   - 无效URL自动标记
   - 失效图片链接替换为默认图片
   - 格式错误的数据自动修正

7.4 核心功能实现方案
7.4.1 API接口设计（基于FastAPI）
主要API端点
模块
端点
方法
功能描述
权限
认证
/api/v1/auth/wechat/qrcode
GET
获取微信登录二维码
公开
认证
/api/v1/auth/wechat/check
GET
检查扫码登录状态
公开
认证
/api/v1/auth/me
GET
获取当前用户信息
登录用户
Agent
/api/v1/agents
GET
获取Agent列表（支持筛选、分页）
公开
Agent
/api/v1/agents/{id}
GET
获取Agent详情
公开
Agent
/api/v1/agents/search
GET
搜索Agent
公开
收藏
/api/v1/favorites
GET
获取用户收藏列表
登录用户
收藏
/api/v1/favorites/{agent_id}
POST
收藏Agent
登录用户
收藏
/api/v1/favorites/{agent_id}
DELETE
取消收藏
登录用户
管理员
/api/v1/admin/agents
POST
创建新Agent
管理员
管理员
/api/v1/admin/agents/{id}
PUT
更新Agent信息
管理员
管理员
/api/v1/admin/agents/{id}
DELETE
删除Agent
管理员
管理员
/api/v1/admin/agents/batch
POST
批量操作Agent
管理员
系统
/api/v1/system/languages
GET
获取支持的语言列表
公开
系统
/api/v1/system/stats
GET
获取系统统计信息
管理员
API请求/响应规范
  - 请求参数：路径参数、查询参数、请求体（JSON格式）
  - 响应格式：
{
  "code": 200,  // 状态码：200成功，其他为错误
  "message": "success",  // 消息描述
  "data": {},  // 业务数据
  "request_id": "req-xxxx-xxxx"  // 请求ID，用于追踪
}
  - 分页响应格式：
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [],  // 列表数据
    "pagination": {
      "total": 100,  // 总条数
      "page": 1,  // 当前页
      "page_size": 20,  // 每页条数
      "pages": 5  // 总页数
    }
  }
}

4.1.1 错误处理和异常情况设计

错误码体系设计：
```json
{
  "code": 4001,
  "message": "用户未登录",
  "data": null,
  "request_id": "req-xxxx-xxxx",
  "error_details": {
    "error_type": "AUTHENTICATION_ERROR",
    "error_code": "USER_NOT_LOGGED_IN",
    "suggestions": ["请先登录", "Please login first"]
  }
}
```

统一错误码定义：
- 2xx 成功状态码
  - 200: 请求成功
  - 201: 创建成功
  - 204: 删除成功（无返回内容）

- 4xx 客户端错误
  - 4000: 请求参数错误
  - 4001: 用户未登录
  - 4003: 权限不足
  - 4004: 资源不存在
  - 4005: 请求频率过高
  - 4006: 数据验证失败
  - 4007: 重复操作
  - 4008: 账号被禁用

- 5xx 服务端错误
  - 5000: 服务器内部错误
  - 5001: 数据库连接失败
  - 5002: 第三方服务不可用
  - 5003: 缓存服务异常
  - 5004: 搜索服务不可用
  - 5005: 文件上传失败

异常场景处理策略：

1. 微信登录异常处理：
   - 二维码生成失败：显示刷新按钮，提供手动重试机制
   - 微信服务不可用：显示友好提示，建议稍后重试
   - 登录超时：自动刷新二维码，提示用户重新扫码
   - 网络异常：前端重试机制，最多重试3次

2. 搜索服务异常处理：
   - Elasticsearch不可用：降级到MongoDB基础搜索
   - 搜索超时：返回缓存结果或提示用户简化搜索条件
   - 索引异常：自动触发索引重建任务

3. 数据采集异常处理：
   - 爬虫任务失败：记录失败原因，自动重试机制（指数退避）
   - 网站反爬虫：调整爬取频率，使用代理池
   - 数据解析失败：人工审核队列，管理员手动处理

4. 文件上传异常处理：
   - 文件过大：前端压缩，后端分片上传
   - 格式不支持：提供格式转换建议
   - 存储空间不足：清理临时文件，告警管理员

前端错误展示规范：
- 全局错误提示：Toast消息，3秒自动消失
- 表单验证错误：字段下方红色提示文字
- 页面级错误：错误页面，提供返回按钮
- 网络错误：加载状态指示器，重试按钮

多语言错误提示：
```json
{
  "error_messages": {
    "zh": {
      "4001": "请先登录后再进行此操作",
      "4003": "您没有权限执行此操作",
      "4004": "请求的资源不存在",
      "5000": "服务器繁忙，请稍后重试"
    },
    "en": {
      "4001": "Please login first to perform this action",
      "4003": "You don't have permission to perform this action", 
      "4004": "The requested resource does not exist",
      "5000": "Server is busy, please try again later"
    }
  }
}
```

系统降级方案：
1. 搜索服务降级：
   - 主搜索引擎故障时，使用MongoDB基础查询
   - 返回有限结果集，提示用户服务降级状态
   
2. 缓存服务降级：
   - Redis不可用时，直接查询数据库
   - 增加数据库连接池大小，应对额外负载
   
3. 第三方服务降级：
   - 微信登录服务异常时，提供邮箱注册备选方案（临时）
   - 图片CDN异常时，使用本地存储备份

监控和告警机制：
- 错误率监控：API错误率超过5%时告警
- 响应时间监控：平均响应时间超过1秒时告警  
- 服务可用性监控：服务不可用时立即告警
- 业务指标监控：搜索成功率、登录成功率等

4.2 微信扫码登录实现
  
  8. 流程设计：
    - 前端请求后端生成微信登录二维码
    - 后端调用微信开放平台接口生成二维码，并关联一个临时会话ID
    - 前端展示二维码，同时轮询后端检查登录状态
    - 用户扫码并确认授权后，微信回调后端接口
    - 后端验证回调信息，获取用户OpenID，创建或更新用户记录
    - 后端生成JWT令牌，关联临时会话ID
    - 前端轮询获取到登录成功状态和JWT令牌，完成登录
  9. 技术实现：
    - 使用wechatpy库处理微信接口交互
    - JWT令牌存储用户身份信息，设置合理过期时间
    - Redis缓存临时会话状态和扫码状态
4.3 数据采集与处理（基于LangChain + LangGraph）

  数据采集策略：
  - 主要方式：智能爬虫系统，确保数据的全面性和时效性
  - 辅助方式：用户贡献机制，用于补充新增或更新的Agent信息
  - 所有用户提交的信息均需经过管理员审核，爬虫采集的数据通过AI验证确保准确性
  
  10. 智能爬虫系统：
    - 基于LangChain的WebBaseLoader和自定义爬虫工具
    - LangGraph构建多智能体协作系统：
      - 调度智能体：负责任务分配和进度管理
      - 采集智能体：负责从指定来源抓取信息
      - 解析智能体：负责提取和清洗关键信息
      - 验证智能体：负责验证信息准确性
  11. 采集来源：
    - 官方网站
    - GitHub仓库
    - 技术博客和媒体报道
    - 融资信息平台（Crunchbase、IT桔子等）
    - 行业报告和研究论文
  12. 处理流程：
定时任务触发 → 调度智能体分配任务 → 采集智能体获取原始数据 → 
解析智能体提取结构化信息 → 验证智能体交叉验证 → 
与现有数据比对 → 更新数据库 → 生成变更日志
4.4 管理员后台功能实现
  
  13. Agent信息管理：
    - 完整的CRUD操作API
    - 支持批量导入/导出
    - 信息变更审计日志
    - 版本历史记录与回滚
  14. 审核流程：
    - 用户提交的Agent信息自动进入待审核队列
    - 管理员可查看、通过、拒绝或编辑待审核内容
    - 审核操作记录完整日志
  15. 系统管理：
    - 用户管理（查看、禁用、角色调整）
    - 数据统计与可视化
    - 爬虫任务监控与管理
    - 系统配置项管理
7.5 安全与性能优化
7.5.1 安全措施
  16. 认证与授权：
    - JWT令牌认证，支持刷新机制
    - 基于角色的访问控制（RBAC）
    - 敏感操作二次验证
  17. 数据安全：
    - 所有API通过HTTPS传输
    - 密码和敏感信息加密存储
    - 输入验证和清洗，防止注入攻击
    - 防暴力破解（登录尝试限制）
  18. API安全：
    - 请求频率限制（Rate Limiting）
    - CORS策略配置
    - API签名机制（针对第三方集成）
7.5.2 性能优化
  19. 数据库优化：
    - MongoDB索引设计（名称、标签、技术栈等）
    - MySQL索引优化（用户ID、时间等）
    - 数据库连接池配置
  20. 缓存策略：
    - Redis缓存热门Agent信息
    - API响应缓存（根据更新频率设置过期时间）
    - 分页查询结果缓存
  21. 异步处理：
    - 数据采集和更新通过Celery异步执行
    - 邮件通知、日志记录等非核心操作异步化
    - 批量操作分批处理，避免长时间阻塞
7.6 部署与运维
7.6.1 部署架构
                     ┌─────────────┐
                     │  负载均衡器  │
                     │   (Nginx)   │
                     └──────┬──────┘
                            │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
┌────────▼────────┐ ┌───────▼──────┐ ┌───────▼──────┐
│  API服务实例1   │ │ API服务实例2  │ │ API服务实例n  │
│  (FastAPI)      │ │  (FastAPI)   │ │  (FastAPI)   │
└────────┬────────┘ └───────┬──────┘ └───────┬──────┘
         │                 │                 │
         └─────────────────┼─────────────────┘
                            │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
┌────────▼────────┐ ┌───────▼──────┐ ┌───────▼──────┐
│    MongoDB      │ │    MySQL     │ │    Redis     │
│  (副本集)       │ │  (主从复制)  │ │  (缓存/队列)  │
└─────────────────┘ └──────────────┘ └──────────────┘
                                            │
                                   ┌─────────▼─────────┐
                                   │   Celery Worker   │
                                   │  (异步任务处理)    │
                                   └───────────────────┘
7.6.2 环境配置和部署参数

开发环境配置（.env.development）：
```bash
# 应用配置
APP_NAME=AgentPedia
APP_VERSION=1.0.0
APP_ENV=development
DEBUG=true
SECRET_KEY=dev-secret-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# 服务端口配置
API_PORT=8000
FRONTEND_PORT=3000
ADMIN_PORT=3001

# 数据库配置
MONGODB_URL=mongodb://localhost:27017/agentpedia_dev
MONGODB_DATABASE=agentpedia_dev
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=agentpedia_dev
MYSQL_USER=dev_user
MYSQL_PASSWORD=dev_password

# Redis配置
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=
REDIS_DB=0

# 微信登录配置
WECHAT_APP_ID=your_dev_app_id
WECHAT_APP_SECRET=your_dev_app_secret
WECHAT_REDIRECT_URI=http://localhost:3000/auth/wechat/callback

# JWT配置
JWT_SECRET_KEY=dev-jwt-secret
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# 文件存储配置
UPLOAD_PATH=./uploads
MAX_FILE_SIZE=10485760  # 10MB
ALLOWED_FILE_TYPES=jpg,jpeg,png,svg,webp

# 搜索引擎配置
ELASTICSEARCH_URL=http://localhost:9200
ELASTICSEARCH_INDEX_PREFIX=agentpedia_dev

# 日志配置
LOG_LEVEL=DEBUG
LOG_FILE=./logs/app.log
LOG_MAX_SIZE=10485760  # 10MB
LOG_BACKUP_COUNT=5

# 邮件配置
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_USE_TLS=true

# 爬虫配置
CRAWLER_DELAY=1
CRAWLER_TIMEOUT=30
CRAWLER_MAX_RETRIES=3
CRAWLER_USER_AGENT=AgentPedia-Bot/1.0

# 缓存配置
CACHE_TTL=3600  # 1小时
SEARCH_CACHE_TTL=1800  # 30分钟
API_RATE_LIMIT=100  # 每分钟100次请求
```

测试环境配置（.env.testing）：
```bash
# 应用配置
APP_ENV=testing
DEBUG=false
SECRET_KEY=test-secret-key-different-from-dev

# 数据库配置（使用独立的测试数据库）
MONGODB_DATABASE=agentpedia_test
MYSQL_DATABASE=agentpedia_test
REDIS_DB=1

# 测试专用配置
TEST_DATA_RESET=true
MOCK_EXTERNAL_APIS=true
SKIP_EMAIL_SENDING=true
FAST_PASSWORD_HASHING=true

# 性能测试配置
LOAD_TEST_USERS=100
LOAD_TEST_DURATION=300  # 5分钟
```

生产环境配置（.env.production）：
```bash
# 应用配置
APP_ENV=production
DEBUG=false
SECRET_KEY=${PRODUCTION_SECRET_KEY}  # 从环境变量或密钥管理服务获取
ALLOWED_HOSTS=agentpedia.com,www.agentpedia.com,api.agentpedia.com

# 服务配置
API_PORT=8000
WORKERS=4  # Gunicorn worker数量
WORKER_CLASS=uvicorn.workers.UvicornWorker
WORKER_CONNECTIONS=1000
MAX_REQUESTS=1000
MAX_REQUESTS_JITTER=100

# 数据库配置（生产环境使用集群）
MONGODB_URL=mongodb://mongo1:27017,mongo2:27017,mongo3:27017/agentpedia?replicaSet=rs0
MONGODB_DATABASE=agentpedia
MYSQL_HOST=mysql-master.internal
MYSQL_READ_HOST=mysql-slave.internal
MYSQL_PORT=3306
MYSQL_DATABASE=agentpedia
MYSQL_USER=${DB_USER}
MYSQL_PASSWORD=${DB_PASSWORD}
MYSQL_POOL_SIZE=20
MYSQL_MAX_OVERFLOW=30

# Redis配置（生产环境使用集群）
REDIS_URL=redis://redis-cluster:6379/0
REDIS_PASSWORD=${REDIS_PASSWORD}
REDIS_SENTINEL_HOSTS=sentinel1:26379,sentinel2:26379,sentinel3:26379
REDIS_MASTER_NAME=mymaster

# SSL/TLS配置
SSL_CERT_PATH=/etc/ssl/certs/agentpedia.crt
SSL_KEY_PATH=/etc/ssl/private/agentpedia.key
FORCE_HTTPS=true
HSTS_MAX_AGE=31536000

# 安全配置
CORS_ORIGINS=https://agentpedia.com,https://www.agentpedia.com
CSRF_TRUSTED_ORIGINS=https://agentpedia.com,https://www.agentpedia.com
SESSION_COOKIE_SECURE=true
CSRF_COOKIE_SECURE=true

# 监控配置
SENTRY_DSN=${SENTRY_DSN}
PROMETHEUS_PORT=9090
HEALTH_CHECK_PATH=/health
METRICS_PATH=/metrics

# 文件存储配置（生产环境使用云存储）
STORAGE_TYPE=s3
AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
AWS_STORAGE_BUCKET_NAME=agentpedia-assets
AWS_S3_REGION_NAME=us-west-2
CDN_DOMAIN=cdn.agentpedia.com

# 搜索引擎配置（生产环境使用集群）
ELASTICSEARCH_HOSTS=es1:9200,es2:9200,es3:9200
ELASTICSEARCH_USERNAME=${ES_USERNAME}
ELASTICSEARCH_PASSWORD=${ES_PASSWORD}
ELASTICSEARCH_USE_SSL=true
ELASTICSEARCH_VERIFY_CERTS=true

# 性能配置
API_RATE_LIMIT=1000  # 每分钟1000次请求
CACHE_TTL=7200  # 2小时
SEARCH_CACHE_TTL=3600  # 1小时
DATABASE_QUERY_TIMEOUT=30
HTTP_TIMEOUT=60

# 备份配置
BACKUP_SCHEDULE=0 2 * * *  # 每天凌晨2点
BACKUP_RETENTION_DAYS=30
BACKUP_S3_BUCKET=agentpedia-backups
```

Docker配置文件：

docker-compose.yml（开发环境）：
```yaml
version: '3.8'

services:
  api:
    build: 
      context: ./backend
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
      - ./uploads:/app/uploads
    environment:
      - APP_ENV=development
    env_file:
      - .env.development
    depends_on:
      - mongodb
      - mysql
      - redis
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
    env_file:
      - .env.development
    command: npm run dev

  mongodb:
    image: mongo:7.0
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    environment:
      - MONGO_INITDB_DATABASE=agentpedia_dev

  mysql:
    image: mysql:8.0
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    environment:
      - MYSQL_ROOT_PASSWORD=root_password
      - MYSQL_DATABASE=agentpedia_dev
      - MYSQL_USER=dev_user
      - MYSQL_PASSWORD=dev_password

  redis:
    image: redis:7.2-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  elasticsearch:
    image: elasticsearch:7.17.0
    ports:
      - "9200:9200"
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    volumes:
      - es_data:/usr/share/elasticsearch/data

volumes:
  mongodb_data:
  mysql_data:
  redis_data:
  es_data:
```

docker-compose.prod.yml（生产环境）：
```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl
    depends_on:
      - api

  api:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    expose:
      - "8000"
    env_file:
      - .env.production
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  celery:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    env_file:
      - .env.production
    command: celery -A app.celery worker --loglevel=info
    deploy:
      replicas: 2

  celery-beat:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    env_file:
      - .env.production
    command: celery -A app.celery beat --loglevel=info

networks:
  default:
    driver: bridge
```

Kubernetes配置示例（k8s-deployment.yaml）：
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agentpedia-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agentpedia-api
  template:
    metadata:
      labels:
        app: agentpedia-api
    spec:
      containers:
      - name: api
        image: agentpedia/api:latest
        ports:
        - containerPort: 8000
        env:
        - name: APP_ENV
          value: "production"
        envFrom:
        - secretRef:
            name: agentpedia-secrets
        - configMapRef:
            name: agentpedia-config
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

部署脚本（deploy.sh）：
```bash
#!/bin/bash

# 部署脚本
set -e

ENV=${1:-development}
echo "Deploying to $ENV environment..."

# 检查环境变量文件
if [ ! -f ".env.$ENV" ]; then
    echo "Error: .env.$ENV file not found!"
    exit 1
fi

# 构建镜像
echo "Building Docker images..."
docker-compose -f docker-compose.yml -f docker-compose.$ENV.yml build

# 运行数据库迁移
echo "Running database migrations..."
docker-compose -f docker-compose.yml -f docker-compose.$ENV.yml run --rm api python manage.py migrate

# 启动服务
echo "Starting services..."
docker-compose -f docker-compose.yml -f docker-compose.$ENV.yml up -d

# 健康检查
echo "Performing health check..."
sleep 30
curl -f http://localhost:8000/health || exit 1

echo "Deployment completed successfully!"
```

7.6.3 容器化部署
  使用Docker和Docker Compose实现容器化部署：
  - 每个服务组件打包为独立Docker镜像
  - Docker Compose管理多容器应用
  - 支持开发、测试、生产环境的不同配置
  - Kubernetes支持水平扩展和高可用部署

7.6.4 测试策略和用例设计

测试金字塔策略：

1. 单元测试（Unit Tests）- 70%
   - 覆盖率目标：≥90%
   - 测试范围：业务逻辑、数据验证、工具函数
   - 测试框架：pytest（后端）、Jest（前端）

后端单元测试用例：
```python
# 测试Agent数据验证
class TestAgentValidation:
    def test_valid_agent_creation(self):
        """测试有效Agent数据创建"""
        agent_data = {
            "name": "ChatGPT",
            "slug": "chatgpt",
            "official_url": "https://chat.openai.com",
            "description": {
                "short": "AI聊天助手",
                "detailed": "OpenAI开发的大型语言模型..."
            }
        }
        agent = Agent(**agent_data)
        assert agent.is_valid()
    
    def test_invalid_slug_format(self):
        """测试无效slug格式"""
        with pytest.raises(ValidationError):
            Agent(slug="Invalid Slug!")
    
    def test_url_accessibility(self):
        """测试URL可访问性"""
        agent = Agent(official_url="https://invalid-url.com")
        assert not agent.validate_url_accessibility()

# 测试搜索功能
class TestSearchService:
    def test_basic_search(self):
        """测试基础搜索功能"""
        results = search_agents("ChatGPT")
        assert len(results) > 0
        assert "chatgpt" in [r.slug for r in results]
    
    def test_multilingual_search(self):
        """测试多语言搜索"""
        cn_results = search_agents("聊天机器人", lang="zh")
        en_results = search_agents("chatbot", lang="en")
        assert len(cn_results) > 0
        assert len(en_results) > 0
    
    def test_search_filters(self):
        """测试搜索过滤器"""
        results = search_agents(
            query="AI",
            filters={"status": "released", "tags": ["NLP"]}
        )
        for result in results:
            assert result.status == "released"
            assert "NLP" in result.tags

# 测试微信登录
class TestWeChatAuth:
    def test_generate_qr_code(self):
        """测试生成二维码"""
        qr_data = generate_wechat_qr()
        assert "qr_code_url" in qr_data
        assert "state" in qr_data
    
    def test_callback_processing(self):
        """测试回调处理"""
        callback_data = {"code": "test_code", "state": "test_state"}
        result = process_wechat_callback(callback_data)
        assert "access_token" in result or "error" in result
```

前端单元测试用例：
```javascript
// 测试搜索组件
describe('SearchComponent', () => {
  test('renders search input', () => {
    render(<SearchComponent />);
    expect(screen.getByPlaceholderText('搜索AI Agent...')).toBeInTheDocument();
  });

  test('handles search input change', () => {
    const mockOnSearch = jest.fn();
    render(<SearchComponent onSearch={mockOnSearch} />);
    
    const input = screen.getByPlaceholderText('搜索AI Agent...');
    fireEvent.change(input, { target: { value: 'ChatGPT' } });
    
    expect(input.value).toBe('ChatGPT');
  });

  test('submits search on enter key', () => {
    const mockOnSearch = jest.fn();
    render(<SearchComponent onSearch={mockOnSearch} />);
    
    const input = screen.getByPlaceholderText('搜索AI Agent...');
    fireEvent.change(input, { target: { value: 'ChatGPT' } });
    fireEvent.keyPress(input, { key: 'Enter', code: 'Enter' });
    
    expect(mockOnSearch).toHaveBeenCalledWith('ChatGPT');
  });
});

// 测试Agent卡片组件
describe('AgentCard', () => {
  const mockAgent = {
    name: 'ChatGPT',
    slug: 'chatgpt',
    description: { short: 'AI聊天助手' },
    logo_url: 'https://example.com/logo.png',
    tags: ['NLP', 'Chat']
  };

  test('displays agent information correctly', () => {
    render(<AgentCard agent={mockAgent} />);
    
    expect(screen.getByText('ChatGPT')).toBeInTheDocument();
    expect(screen.getByText('AI聊天助手')).toBeInTheDocument();
    expect(screen.getByText('NLP')).toBeInTheDocument();
    expect(screen.getByText('Chat')).toBeInTheDocument();
  });

  test('handles favorite button click', () => {
    const mockOnFavorite = jest.fn();
    render(<AgentCard agent={mockAgent} onFavorite={mockOnFavorite} />);
    
    const favoriteButton = screen.getByRole('button', { name: /收藏/ });
    fireEvent.click(favoriteButton);
    
    expect(mockOnFavorite).toHaveBeenCalledWith('chatgpt');
  });
});
```

2. 集成测试（Integration Tests）- 20%
   - 测试API端点集成
   - 数据库操作集成
   - 第三方服务集成

集成测试用例：
```python
# API集成测试
class TestAPIIntegration:
    def test_agent_crud_operations(self):
        """测试Agent CRUD操作"""
        # 创建
        response = client.post("/api/agents", json=valid_agent_data)
        assert response.status_code == 201
        agent_id = response.json()["data"]["id"]
        
        # 读取
        response = client.get(f"/api/agents/{agent_id}")
        assert response.status_code == 200
        
        # 更新
        update_data = {"description": {"short": "更新的描述"}}
        response = client.put(f"/api/agents/{agent_id}", json=update_data)
        assert response.status_code == 200
        
        # 删除
        response = client.delete(f"/api/agents/{agent_id}")
        assert response.status_code == 204
    
    def test_search_api_integration(self):
        """测试搜索API集成"""
        # 基础搜索
        response = client.get("/api/search?q=ChatGPT")
        assert response.status_code == 200
        assert len(response.json()["data"]["results"]) > 0
        
        # 带过滤器搜索
        response = client.get("/api/search?q=AI&status=released&tags=NLP")
        assert response.status_code == 200
        
        # 分页搜索
        response = client.get("/api/search?q=AI&page=1&size=10")
        assert response.status_code == 200
        assert "pagination" in response.json()["data"]

# 数据库集成测试
class TestDatabaseIntegration:
    def test_mongodb_operations(self):
        """测试MongoDB操作"""
        # 插入文档
        agent_doc = {"name": "Test Agent", "slug": "test-agent"}
        result = db.agents.insert_one(agent_doc)
        assert result.inserted_id
        
        # 查询文档
        found_agent = db.agents.find_one({"slug": "test-agent"})
        assert found_agent["name"] == "Test Agent"
        
        # 更新文档
        db.agents.update_one(
            {"slug": "test-agent"},
            {"$set": {"name": "Updated Agent"}}
        )
        updated_agent = db.agents.find_one({"slug": "test-agent"})
        assert updated_agent["name"] == "Updated Agent"
    
    def test_mysql_operations(self):
        """测试MySQL操作"""
        # 创建用户
        user = User(openid="test_openid", nickname="Test User")
        db.session.add(user)
        db.session.commit()
        
        # 添加收藏
        favorite = UserFavorite(user_id=user.id, agent_id="test_agent_id")
        db.session.add(favorite)
        db.session.commit()
        
        # 查询收藏
        user_favorites = UserFavorite.query.filter_by(user_id=user.id).all()
        assert len(user_favorites) == 1
```

3. 端到端测试（E2E Tests）- 10%
   - 用户完整流程测试
   - 跨浏览器兼容性测试
   - 测试框架：Playwright

E2E测试用例：
```javascript
// 用户搜索流程测试
test('用户搜索Agent完整流程', async ({ page }) => {
  // 访问首页
  await page.goto('/');
  
  // 搜索Agent
  await page.fill('[data-testid="search-input"]', 'ChatGPT');
  await page.press('[data-testid="search-input"]', 'Enter');
  
  // 验证搜索结果
  await expect(page.locator('[data-testid="search-results"]')).toBeVisible();
  await expect(page.locator('[data-testid="agent-card"]').first()).toBeVisible();
  
  // 点击Agent详情
  await page.click('[data-testid="agent-card"]');
  
  // 验证详情页
  await expect(page.locator('[data-testid="agent-detail"]')).toBeVisible();
  await expect(page.locator('h1')).toContainText('ChatGPT');
});

// 用户登录收藏流程测试
test('用户登录并收藏Agent', async ({ page }) => {
  await page.goto('/');
  
  // 点击登录
  await page.click('[data-testid="login-button"]');
  
  // 模拟微信扫码登录（测试环境）
  await page.click('[data-testid="mock-wechat-login"]');
  
  // 验证登录成功
  await expect(page.locator('[data-testid="user-avatar"]')).toBeVisible();
  
  // 搜索并收藏Agent
  await page.fill('[data-testid="search-input"]', 'ChatGPT');
  await page.press('[data-testid="search-input"]', 'Enter');
  await page.click('[data-testid="favorite-button"]');
  
  // 验证收藏成功
  await expect(page.locator('[data-testid="favorite-success"]')).toBeVisible();
  
  // 查看个人中心
  await page.click('[data-testid="user-center"]');
  await expect(page.locator('[data-testid="favorite-list"]')).toContainText('ChatGPT');
});
```

性能测试：

1. 负载测试
```python
# 使用Locust进行负载测试
from locust import HttpUser, task, between

class AgentPediaUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def search_agents(self):
        """搜索Agent（高频操作）"""
        self.client.get("/api/search?q=AI")
    
    @task(2)
    def view_agent_detail(self):
        """查看Agent详情"""
        self.client.get("/api/agents/chatgpt")
    
    @task(1)
    def user_favorites(self):
        """用户收藏操作"""
        self.client.post("/api/favorites", json={"agent_id": "chatgpt"})
    
    def on_start(self):
        """模拟用户登录"""
        self.client.post("/api/auth/login", json={
            "openid": "test_user",
            "nickname": "Test User"
        })
```

2. 压力测试配置
```bash
# 压力测试命令
locust -f performance_tests.py --host=http://localhost:8000 \
       --users=1000 --spawn-rate=10 --run-time=300s

# 性能指标要求
- API响应时间：P95 < 500ms
- 搜索响应时间：P95 < 200ms
- 并发用户数：≥1000
- 系统可用性：≥99.9%
```

安全测试：

1. 安全扫描
```python
# SQL注入测试
def test_sql_injection():
    malicious_inputs = [
        "'; DROP TABLE users; --",
        "1' OR '1'='1",
        "admin'/*",
    ]
    for input_data in malicious_inputs:
        response = client.get(f"/api/search?q={input_data}")
        assert response.status_code != 500  # 不应该导致服务器错误

# XSS测试
def test_xss_prevention():
    xss_payloads = [
        "<script>alert('XSS')</script>",
        "javascript:alert('XSS')",
        "<img src=x onerror=alert('XSS')>",
    ]
    for payload in xss_payloads:
        response = client.post("/api/agents", json={
            "name": payload,
            "description": {"short": payload}
        })
        # 验证输出已被转义
        if response.status_code == 201:
            agent_data = response.json()["data"]
            assert "<script>" not in agent_data["name"]
```

测试自动化流程：

1. CI/CD集成
```yaml
# .github/workflows/test.yml
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      mongodb:
        image: mongo:7.0
        ports:
          - 27017:27017
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: root
          MYSQL_DATABASE: test_db
        ports:
          - 3306:3306
      redis:
        image: redis:7.2-alpine
        ports:
          - 6379:6379
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Run unit tests
      run: |
        pytest tests/unit/ --cov=app --cov-report=xml
    
    - name: Run integration tests
      run: |
        pytest tests/integration/
    
    - name: Run E2E tests
      run: |
        npm install
        npx playwright install
        npm run test:e2e
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

2. 测试数据管理
```python
# 测试数据工厂
class AgentFactory:
    @staticmethod
    def create_agent(**kwargs):
        default_data = {
            "name": "Test Agent",
            "slug": "test-agent",
            "official_url": "https://example.com",
            "description": {
                "short": "测试Agent",
                "detailed": "这是一个测试用的Agent"
            },
            "status": "released",
            "tags": ["test"]
        }
        default_data.update(kwargs)
        return default_data
    
    @staticmethod
    def create_batch_agents(count=10):
        return [
            AgentFactory.create_agent(
                name=f"Agent {i}",
                slug=f"agent-{i}"
            ) for i in range(count)
        ]

# 测试数据清理
@pytest.fixture(autouse=True)
def cleanup_test_data():
    yield
    # 清理测试数据
    db.agents.delete_many({"slug": {"$regex": "^test-"}})
    User.query.filter(User.openid.like('test_%')).delete()
    db.session.commit()
```

测试报告和监控：

1. 测试覆盖率报告
2. 性能测试报告
3. 安全扫描报告
4. 测试执行趋势分析
5. 缺陷跟踪和修复状态

7.6.4 监控与日志
  22. 监控系统：
    - Prometheus + Grafana监控系统指标
    - 服务健康检查接口
    - 关键业务指标监控（API响应时间、错误率等）
  23. 日志管理：
    - 集中式日志收集（ELK Stack）
    - 分级日志（DEBUG/INFO/WARN/ERROR）
    - 关键操作审计日志

7.6.5 数据迁移和版本升级方案

版本管理策略：

1. 语义化版本控制（Semantic Versioning）
   - 格式：MAJOR.MINOR.PATCH (例如：1.2.3)
   - MAJOR：不兼容的API修改
   - MINOR：向后兼容的功能性新增
   - PATCH：向后兼容的问题修正

2. 版本发布流程
   - 开发版本：dev-YYYYMMDD-commit_hash
   - 测试版本：rc-1.2.3-rc.1
   - 正式版本：1.2.3
   - 热修复版本：1.2.3-hotfix.1

数据库迁移方案：

1. MySQL数据库迁移
```python
# 迁移管理器
import os
import mysql.connector
from datetime import datetime
import logging

class MySQLMigrationManager:
    def __init__(self, config):
        self.config = config
        self.connection = None
        self.logger = logging.getLogger(__name__)
    
    def connect(self):
        """连接数据库"""
        self.connection = mysql.connector.connect(**self.config)
        self.connection.autocommit = False
    
    def create_migration_table(self):
        """创建迁移记录表"""
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                id INT PRIMARY KEY AUTO_INCREMENT,
                version VARCHAR(50) UNIQUE NOT NULL,
                description TEXT,
                executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                execution_time_ms INT,
                checksum VARCHAR(64),
                success BOOLEAN DEFAULT TRUE
            )
        """)
        self.connection.commit()
    
    def get_current_version(self):
        """获取当前数据库版本"""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT version FROM schema_migrations 
            WHERE success = TRUE 
            ORDER BY executed_at DESC 
            LIMIT 1
        """)
        result = cursor.fetchone()
        return result[0] if result else None
    
    def execute_migration(self, migration_file):
        """执行单个迁移文件"""
        start_time = datetime.now()
        
        try:
            with open(migration_file, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            # 计算校验和
            import hashlib
            checksum = hashlib.sha256(sql_content.encode()).hexdigest()
            
            # 执行迁移SQL
            cursor = self.connection.cursor()
            for statement in sql_content.split(';'):
                if statement.strip():
                    cursor.execute(statement)
            
            # 记录迁移
            version = os.path.basename(migration_file).split('_')[0]
            description = os.path.basename(migration_file).split('_', 1)[1].replace('.sql', '')
            execution_time = int((datetime.now() - start_time).total_seconds() * 1000)
            
            cursor.execute("""
                INSERT INTO schema_migrations 
                (version, description, execution_time_ms, checksum) 
                VALUES (%s, %s, %s, %s)
            """, (version, description, execution_time, checksum))
            
            self.connection.commit()
            self.logger.info(f"Migration {version} executed successfully")
            
        except Exception as e:
            self.connection.rollback()
            self.logger.error(f"Migration {version} failed: {str(e)}")
            raise
    
    def migrate_to_version(self, target_version=None):
        """迁移到指定版本"""
        migration_dir = "migrations/mysql"
        migration_files = sorted([
            f for f in os.listdir(migration_dir) 
            if f.endswith('.sql')
        ])
        
        current_version = self.get_current_version()
        
        for migration_file in migration_files:
            version = migration_file.split('_')[0]
            
            # 跳过已执行的迁移
            if current_version and version <= current_version:
                continue
            
            # 如果指定了目标版本，检查是否超过
            if target_version and version > target_version:
                break
            
            self.execute_migration(os.path.join(migration_dir, migration_file))

# 迁移文件示例
# migrations/mysql/001_create_users_table.sql
"""
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    openid VARCHAR(100) UNIQUE NOT NULL,
    nickname VARCHAR(100),
    avatar_url VARCHAR(500),
    role ENUM('guest', 'user', 'contributor', 'moderator', 'admin', 'super_admin') DEFAULT 'user',
    status ENUM('active', 'disabled', 'banned') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_openid ON users(openid);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_status ON users(status);
"""

# migrations/mysql/002_add_user_statistics.sql
"""
ALTER TABLE users 
ADD COLUMN submitted_agents_count INT DEFAULT 0,
ADD COLUMN approved_agents_count INT DEFAULT 0,
ADD COLUMN contribution_score INT DEFAULT 0,
ADD COLUMN last_login_at TIMESTAMP NULL;

CREATE INDEX idx_users_contribution_score ON users(contribution_score);
"""
```

2. MongoDB数据迁移
```python
from pymongo import MongoClient
import json
from datetime import datetime

class MongoMigrationManager:
    def __init__(self, config):
        self.client = MongoClient(config['uri'])
        self.db = self.client[config['database']]
        self.migrations_collection = self.db.schema_migrations
    
    def get_current_version(self):
        """获取当前MongoDB版本"""
        result = self.migrations_collection.find_one(
            {"success": True},
            sort=[("executed_at", -1)]
        )
        return result['version'] if result else None
    
    def execute_migration(self, migration_module):
        """执行MongoDB迁移"""
        start_time = datetime.now()
        
        try:
            # 执行迁移逻辑
            migration_module.up(self.db)
            
            # 记录迁移
            execution_time = int((datetime.now() - start_time).total_seconds() * 1000)
            self.migrations_collection.insert_one({
                "version": migration_module.VERSION,
                "description": migration_module.DESCRIPTION,
                "executed_at": datetime.now(),
                "execution_time_ms": execution_time,
                "success": True
            })
            
            print(f"MongoDB migration {migration_module.VERSION} completed")
            
        except Exception as e:
            self.migrations_collection.insert_one({
                "version": migration_module.VERSION,
                "description": migration_module.DESCRIPTION,
                "executed_at": datetime.now(),
                "success": False,
                "error": str(e)
            })
            raise

# MongoDB迁移示例
# migrations/mongodb/001_create_agents_collection.py
"""
VERSION = "001"
DESCRIPTION = "Create agents collection with indexes"

def up(db):
    # 创建agents集合
    agents = db.agents
    
    # 创建索引
    agents.create_index("slug", unique=True)
    agents.create_index("name")
    agents.create_index("category")
    agents.create_index("tech_stack")
    agents.create_index("status")
    agents.create_index("created_at")
    agents.create_index([("name", "text"), ("description", "text")])
    
    # 创建初始数据
    if agents.count_documents({}) == 0:
        sample_agent = {
            "name": "ChatGPT",
            "slug": "chatgpt",
            "description": "OpenAI's conversational AI assistant",
            "category": "conversational",
            "tech_stack": ["transformer", "gpt"],
            "status": "active",
            "created_at": datetime.now()
        }
        agents.insert_one(sample_agent)

def down(db):
    # 回滚操作
    db.agents.drop()
"""
```

3. 数据备份和恢复策略
```bash
#!/bin/bash
# backup_script.sh

# 配置
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
MYSQL_BACKUP_FILE="$BACKUP_DIR/mysql_backup_$DATE.sql"
MONGO_BACKUP_DIR="$BACKUP_DIR/mongodb_backup_$DATE"

# MySQL备份
echo "Starting MySQL backup..."
mysqldump \
    --host=$MYSQL_HOST \
    --user=$MYSQL_USER \
    --password=$MYSQL_PASSWORD \
    --single-transaction \
    --routines \
    --triggers \
    $MYSQL_DATABASE > $MYSQL_BACKUP_FILE

# 压缩MySQL备份
gzip $MYSQL_BACKUP_FILE

# MongoDB备份
echo "Starting MongoDB backup..."
mongodump \
    --host=$MONGO_HOST \
    --db=$MONGO_DATABASE \
    --out=$MONGO_BACKUP_DIR

# 压缩MongoDB备份
tar -czf "$MONGO_BACKUP_DIR.tar.gz" -C $BACKUP_DIR "mongodb_backup_$DATE"
rm -rf $MONGO_BACKUP_DIR

# 清理旧备份（保留30天）
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete

echo "Backup completed: $DATE"

# 恢复脚本示例
# restore_mysql.sh
#!/bin/bash
BACKUP_FILE=$1
if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file>"
    exit 1
fi

echo "Restoring MySQL from $BACKUP_FILE..."
gunzip -c $BACKUP_FILE | mysql \
    --host=$MYSQL_HOST \
    --user=$MYSQL_USER \
    --password=$MYSQL_PASSWORD \
    $MYSQL_DATABASE

echo "MySQL restore completed"
```

4. 应用版本升级流程
```python
# 版本升级管理器
class ApplicationUpgradeManager:
    def __init__(self, config):
        self.config = config
        self.current_version = self.get_current_version()
    
    def get_current_version(self):
        """获取当前应用版本"""
        try:
            with open('VERSION', 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return "0.0.0"
    
    def pre_upgrade_checks(self, target_version):
        """升级前检查"""
        checks = []
        
        # 检查磁盘空间
        import shutil
        free_space = shutil.disk_usage('/').free
        if free_space < 1024 * 1024 * 1024:  # 1GB
            checks.append("Insufficient disk space")
        
        # 检查数据库连接
        try:
            # 测试数据库连接
            pass
        except Exception as e:
            checks.append(f"Database connection failed: {e}")
        
        # 检查依赖服务
        services = ['redis', 'elasticsearch']
        for service in services:
            if not self.check_service_health(service):
                checks.append(f"Service {service} is not healthy")
        
        return checks
    
    def backup_before_upgrade(self):
        """升级前备份"""
        import subprocess
        
        # 执行备份脚本
        result = subprocess.run(['./backup_script.sh'], capture_output=True)
        if result.returncode != 0:
            raise Exception(f"Backup failed: {result.stderr}")
        
        return result.stdout.decode()
    
    def upgrade_to_version(self, target_version):
        """升级到指定版本"""
        try:
            # 1. 升级前检查
            issues = self.pre_upgrade_checks(target_version)
            if issues:
                raise Exception(f"Pre-upgrade checks failed: {issues}")
            
            # 2. 备份
            backup_info = self.backup_before_upgrade()
            print(f"Backup completed: {backup_info}")
            
            # 3. 停止服务
            self.stop_services()
            
            # 4. 执行数据库迁移
            self.run_database_migrations(target_version)
            
            # 5. 更新应用代码
            self.update_application_code(target_version)
            
            # 6. 更新配置文件
            self.update_configurations(target_version)
            
            # 7. 启动服务
            self.start_services()
            
            # 8. 健康检查
            if not self.health_check():
                raise Exception("Health check failed after upgrade")
            
            # 9. 更新版本文件
            with open('VERSION', 'w') as f:
                f.write(target_version)
            
            print(f"Successfully upgraded to version {target_version}")
            
        except Exception as e:
            print(f"Upgrade failed: {e}")
            # 回滚逻辑
            self.rollback_upgrade(backup_info)
            raise
    
    def rollback_upgrade(self, backup_info):
        """回滚升级"""
        print("Starting rollback...")
        
        # 停止服务
        self.stop_services()
        
        # 恢复数据库
        self.restore_database(backup_info)
        
        # 恢复应用代码
        self.restore_application_code()
        
        # 启动服务
        self.start_services()
        
        print("Rollback completed")
```

5. 零停机升级策略
```yaml
# 蓝绿部署配置
# docker-compose.blue-green.yml
version: '3.8'

services:
  # 蓝色环境
  api-blue:
    image: agentpedia:${BLUE_VERSION}
    environment:
      - ENV=production
      - DB_SUFFIX=_blue
    networks:
      - blue-network
    deploy:
      replicas: 3

  # 绿色环境
  api-green:
    image: agentpedia:${GREEN_VERSION}
    environment:
      - ENV=production
      - DB_SUFFIX=_green
    networks:
      - green-network
    deploy:
      replicas: 3

  # 负载均衡器
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - api-blue
      - api-green

networks:
  blue-network:
  green-network:
```

6. 数据一致性检查
```python
class DataConsistencyChecker:
    def __init__(self, mysql_config, mongo_config):
        self.mysql_conn = mysql.connector.connect(**mysql_config)
        self.mongo_client = MongoClient(mongo_config['uri'])
        self.mongo_db = self.mongo_client[mongo_config['database']]
    
    def check_user_agent_consistency(self):
        """检查用户和Agent数据一致性"""
        issues = []
        
        # 检查MySQL中的用户是否在MongoDB中有对应的Agent
        mysql_cursor = self.mysql_conn.cursor()
        mysql_cursor.execute("SELECT id, openid FROM users")
        
        for user_id, openid in mysql_cursor.fetchall():
            # 检查用户收藏的Agent是否存在
            mysql_cursor.execute(
                "SELECT agent_slug FROM user_favorites WHERE user_id = %s",
                (user_id,)
            )
            
            for (agent_slug,) in mysql_cursor.fetchall():
                agent = self.mongo_db.agents.find_one({"slug": agent_slug})
                if not agent:
                    issues.append(f"User {openid} has favorite for non-existent agent: {agent_slug}")
        
        return issues
    
    def check_data_integrity(self):
        """全面数据完整性检查"""
        all_issues = []
        
        # 检查各种数据一致性
        all_issues.extend(self.check_user_agent_consistency())
        all_issues.extend(self.check_orphaned_records())
        all_issues.extend(self.check_data_format())
        
        return all_issues
    
    def auto_fix_issues(self, issues):
        """自动修复数据问题"""
        fixed_count = 0
        
        for issue in issues:
            try:
                if "non-existent agent" in issue:
                    # 删除无效的收藏记录
                    agent_slug = issue.split(": ")[-1]
                    mysql_cursor = self.mysql_conn.cursor()
                    mysql_cursor.execute(
                        "DELETE FROM user_favorites WHERE agent_slug = %s",
                        (agent_slug,)
                    )
                    self.mysql_conn.commit()
                    fixed_count += 1
                    
            except Exception as e:
                print(f"Failed to fix issue: {issue}, Error: {e}")
        
        return fixed_count
```

7. 版本兼容性矩阵
```python
COMPATIBILITY_MATRIX = {
    "1.0.0": {
        "database_version": "1.0",
        "api_version": "v1",
        "compatible_clients": ["web-1.0.x", "mobile-1.0.x"],
        "breaking_changes": []
    },
    "1.1.0": {
        "database_version": "1.1",
        "api_version": "v1",
        "compatible_clients": ["web-1.0.x", "web-1.1.x", "mobile-1.0.x"],
        "breaking_changes": []
    },
    "2.0.0": {
        "database_version": "2.0",
        "api_version": "v2",
        "compatible_clients": ["web-2.0.x", "mobile-2.0.x"],
        "breaking_changes": [
            "API response format changed",
            "Authentication method updated",
            "Database schema restructured"
        ]
    }
}

def check_upgrade_compatibility(current_version, target_version):
    """检查版本升级兼容性"""
    current_info = COMPATIBILITY_MATRIX.get(current_version)
    target_info = COMPATIBILITY_MATRIX.get(target_version)
    
    if not current_info or not target_info:
        return False, "Version not found in compatibility matrix"
    
    # 检查是否有破坏性变更
    if target_info["breaking_changes"]:
        return False, f"Breaking changes detected: {target_info['breaking_changes']}"
    
    return True, "Compatible upgrade"
```

监控和告警：

1. 升级过程监控
   - 升级进度实时跟踪
   - 关键指标监控（响应时间、错误率）
   - 自动回滚触发条件

2. 数据迁移监控
   - 迁移进度和性能监控
   - 数据一致性实时检查
   - 迁移失败自动告警

3. 版本管理最佳实践
   - 渐进式发布（金丝雀部署）
   - A/B测试支持
   - 特性开关（Feature Flags）
   - 自动化测试覆盖
  