export default {
  'enableHotkeys': {
    'newUI': {
      'title': '标记快捷键',
      'description': '允许使用快捷键快速选择标签',
    },
    'description': 'Enable labeling hotkeys',
    'onChangeEvent': 'toggleHotkeys',
    'defaultValue': true,
  },
  'enableTooltips': {
    'newUI': {
      'title': '在工具提示上显示快捷键',
      'description': '显示工具和操作工具提示上的键绑定',
    },
    'description': 'Show hotkey tooltips',
    'onChangeEvent': 'toggleTooltips',
    'checked': '',
    'defaultValue': false,
  },
  'enableLabelTooltips': {
    'newUI': {
      'title': '在标签上显示快捷键',
      'description': '显示标签上的快捷键绑定',
    },
    'description': 'Show labels hotkey tooltips',
    'onChangeEvent': 'toggleLabelTooltips',
    'defaultValue': true,
  },
  'showLabels': {
    'newUI': {
      'title': '显示区域标签',
      'description': '显示区域标签名称',
    },
    'description': 'Show labels inside the regions',
    'onChangeEvent': 'toggleShowLabels',
    'defaultValue': false,
  },
  'continuousLabeling': {
    'newUI': {
      'title': '创建区域后保持标签选中',
      'description': '允许使用所选标签连续创建区域',
    },
    'description': 'Keep label selected after creating a region',
    'onChangeEvent': 'toggleContinuousLabeling',
    'defaultValue': false,
  },
  'selectAfterCreate': {
    'newUI': {
      'title': '创建后选择区域',
      'description': '自动选择新建区域',
    },
    'description': 'Select regions after creating',
    'onChangeEvent': 'toggleSelectAfterCreate',
    'defaultValue': false,
  },
  'showLineNumbers': {
    'newUI': {
      'tags': 'Text Tag',
      'title': '显示行号',
      'description': '识别并引用文档中的特定文本行',
    },
    'description': 'Show line numbers for Text',
    'onChangeEvent': 'toggleShowLineNumbers',
    'defaultValue': false,
  },
  'preserveSelectedTool': {
    'newUI': {
      'tags': 'Image Tag',
      'title': '保留所选工具',
      'description': '跨任务保持所选工具',
    },
    'description': 'Remember Selected Tool',
    'onChangeEvent': 'togglepreserveSelectedTool',
    'defaultValue': true,
  },
  'enableSmoothing': {
    'newUI': {
      'tags': 'Image Tag',
      'title': '缩放时的像素平滑',
      'description': '放大时使图像像素平滑',
    },
    'description': 'Enable image smoothing when zoom',
    'onChangeEvent': 'toggleSmoothing',
    'defaultValue': true,
  },
};

