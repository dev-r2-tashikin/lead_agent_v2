
### **SOP: The Annotated URL Exploration Plan for Intelligent Automation**

**/* 全局指令 (Global Directive): AI，当你根据此SOP生成计划时，必须遵循以下规则：
1.  输出必须是一个严格编号的、按顺序执行的【任务列表】。
2.  禁止使用“了解”、“分析”、“研究”等模糊动词。必须使用命令式动词，如“访问 (Visit)”、“提取 (Extract)”、“匹配 (Match)”、“设置变量 (Set Variable)”、“删除 (Delete)”、“跳转 (GOTO)”。
3.  计划必须明确显示状态（如变量的值）和控制流（如条件判断和跳转）。
*/**

---

#### **Phase 0: 绝对净化 (Absolute Purification)**

*   **SOP:**
    1.  立即删除所有被分类为 **[第9类]** 和 **[第10类]** 的URL。
    2.  对剩余的1-8类URL列表执行以下操作：在访问任何URL之前，先进行一次快速的域名/路径扫描。如果URL明显与目标公司无关（例如，一个完全不相关的公司博客），立即删除。

*   **// Annotation for AI:**
    *   `// 计划应显示此阶段的输出是一个经过初步过滤的URL列表，将作为Phase 1的输入。`

---

#### **Phase 1: 确立并验证锚点 (Anchor Identification & Validation)**

*   **SOP:**
    1.  声明一个变量 `Official_Website_URL`，并初始化为 `null`。
    2.  严格按照 **[第1类] -> [第3类], [第2类] -> [第5类], [第7类]** 的优先级顺序探索URL。
    3.  对于探索的每一个URL，必须先执行“相关性检查”。检查页面内容是否明确包含“目标公司”的准确名称。如果不相关，立即删除该URL，并处理下一个。
    4.  如果相关，则尝试提取官网链接。一旦成功，立即将值存入 `Official_Website_URL`，然后停止本阶段，并跳转到 Phase 2。
    5.  如果探索完所有相关类别的URL后 `Official_Website_URL` 仍为 `null`，终止对该公司的所有处理。

*   **// Annotation for AI:**
    *   `// 计划必须在开头声明变量: "任务1: SET Official_Website_URL = null"。`
    *   `// 对于每个被探索的URL，计划必须包含一个明确的【子任务：相关性检查】。`
    *   `// 计划必须展示条件逻辑。例如: "IF 相关性检查==FAIL, THEN Task_Next: DELETE URL AND GOTO next_URL_in_queue"。`
    *   `// 计划必须展示赋值和控制跳转。例如: "IF 官网提取成功, THEN Task_Next: SET Official_Website_URL = '...' AND GOTO Phase 2"。`
    *   `// 计划的最后必须有一个明确的终止条件检查。`

---

#### **Phase 2: 核心刮取与关系判定 (Core Scraping & Role Definition)**

*   **SOP:**
    1.  **子阶段2A - 官网深度刮取：** 只处理 `Official_Website_URL` 及其同域名的URL（主要来自**第1类**和**第6类**）。提取联系方式、产品线、官方动态，并扫描关键词判定其自身是否为分销商。
    2.  **子阶段2B - 第三方关系判定：** 处理所有**非官网**的、且已通过相关性验证的URL。扫描其内容，寻找 **“目标公司名称” + “分销商/partner”** 的组合，以判定目标公司是否为别人的分销商。

*   **// Annotation for AI:**
    *   `// 计划必须明确划分两个子阶段：2A 和 2B。`
    *   `// 对于子阶段2A，所有任务必须明确指出它们的目标是 'Official_Website_URL' 变量所指向的域名。`
    *   `// 提取任务必须具体。错误：“提取联系方式”。正确：“访问 Official_Website_URL + '/contact'，使用正则表达式 '...' 提取Email。”`
    *   `// 对于子阶段2B，计划必须对每个URL重复【相关性检查】和【角色定义检查】这两个步骤。`
    *   `// 角色定义检查必须具体。例如：“在URL X的HTML中，搜索是否存在 "目标公司名" 和 ( "distributor" OR "reseller" ) 同时出现。”`

---

#### **Phase 3: 情报增强 (Intelligence Augmentation)**

*   **SOP:**
    1.  处理**第7类**URL，提取新闻标题和日期，补充近期动态。
    2.  处理**第8类**URL，提取招聘的“职位名称”，生成一个“目标职位画像”列表。
    3.  处理**第3类**URL，使用上一步生成的“目标职位画像”列表作为关键词，在LinkedIn员工中搜索，定位决策人。

*   **// Annotation for AI:**
    *   `// 计划必须显示清晰的数据流。`
    *   `// 处理第8类URL的任务，其输出必须明确为一个【列表变量】，例如: "SET Target_Job_Titles = ['Sourcing Manager', 'Director of Procurement']"。`
    *   `// 处理第3类URL的任务，其输入必须明确引用上一步的变量。例如: "在LinkedIn员工搜索框中，输入 Target_Job_Titles 列表中的每一个词条"。`

---

#### **Phase 4: 系统扩展与归档 (System Scaling & Archiving)**

*   **SOP:**
    1.  处理**第4类**和**第5类**URL：只提取新的公司名称，将其添加到主任务队列中，不进行深度分析。
    2.  处理**第2类**URL：将其标记为“可选验证源”，供后续按需调用。

*   **// Annotation for AI:**
    *   `// 计划必须明确指出，处理第4类和第5类URL的产出是【添加到全局任务队列】，而不是填充当前公司的数据对象。`
    *   `// 计划对于第2类URL的最终指令应该是 "MARK URL as 'Verification_Source' AND ARCHIVE"，而不是“分析”。`

