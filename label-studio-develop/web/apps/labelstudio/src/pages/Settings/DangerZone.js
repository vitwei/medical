import { useMemo, useState } from "react";
import { useHistory } from "react-router";
import { Button } from "../../components";
import { Label } from "../../components/Form";
import { confirm } from "../../components/Modal/Modal";
import { Space } from "../../components/Space/Space";
import { Spinner } from "../../components/Spinner/Spinner";
import { useAPI } from "../../providers/ApiProvider";
import { useProject } from "../../providers/ProjectProvider";

export const DangerZone = () => {
  const { project } = useProject();
  const api = useAPI();
  const history = useHistory();
  const [processing, setProcessing] = useState(null);

  const handleOnClick = (type) => () => {
    confirm({
      title: "选项确认",
      body: "您即将删除所有内容。此操作无法撤消",
      okText: "确认执行",
      buttonLook: "destructive",
      onOk: async () => {
        setProcessing(type);
        if (type === 'annotations') {
          // console.log('delete annotations');
        } else if (type === 'tasks') {
          // console.log('delete tasks');
        } else if (type === 'predictions') {
          // console.log('delete predictions');
        } else if (type === 'reset_cache') {
          await api.callApi('projectResetCache', {
            params: {
              pk: project.id,
            },
          });
        } else if (type === 'tabs') {
          await api.callApi('deleteTabs', {
            body: {
              project: project.id,
            },
          });
        } else if (type === 'project') {
          await api.callApi('deleteProject', {
            params: {
              pk: project.id,
            },
          });
          history.replace('/projects');
        }
        setProcessing(null);
      },
    });
  };

  const buttons = useMemo(() => [{
    type: 'annotations',
    disabled: true, //&& !project.total_annotations_number,
    label: `删除 ${project.total_annotations_number} 标注`,
  }, {
    type: 'tasks',
    disabled: true, //&& !project.task_number,
    label: `删除 ${project.task_number} 任务`,
  }, {
    type: 'predictions',
    disabled: true, //&& !project.total_predictions_number,
    label: `删除 ${project.total_predictions_number} 预测`,
  }, {
    type: 'reset_cache',
    help:
      '如果由于现有标签的验证错误而无法修改标签配置' +
      '但您确信标签不存在，则重置缓存可能会有所帮助' +
      '您可以使用此操作重置缓存，然后重试',
    label: `重置缓存`,
  }, {
    type: 'tabs',
    help: '如果数据管理器未加载, 删除所有数据管理器页标签可以帮助你',
    label: `删除所有页签`,
  }, {
    type: 'project',
    help: '删除项目会从数据库中删除所有任务、标注和项目数据',
    label: '删除该项目',
  }], [project]);

  return (
    <div style={{ width: 480 }}>
      <Label
        text="删除注释、任务或项目"
        description="执行这些操作的风险自负。无法恢复您在此页面上执行的操作。确保您的数据已备份"
        style={{ display: 'block', width: 415 }}
      />

      {project.id ? (
        <Space direction="vertical" spread style={{ marginTop: 32 }}>
          {buttons.map((btn) => {
            const waiting = processing === btn.type;
            const disabled = btn.disabled || (processing && !waiting);

            return (btn.disabled !== true) && (
              <div>
                {btn.help && <Label description={btn.help} style={{ width: 600, display: 'block' }} />}
                <Button
                  key={btn.type}
                  look="danger"
                  disabled={disabled}
                  waiting={waiting}
                  onClick={handleOnClick(btn.type)}
                  style={{ marginLeft: 16, marginTop: 10 }}
                >
                  {btn.label}
                </Button>
              </div>
            );
          })}
        </Space>
      ) : (
        <div style={{ display: "flex", justifyContent: "center", marginTop: 32 }}>
          <Spinner size={32}/>
        </div>
      )}
    </div>
  );
};

DangerZone.title = "危险区域";
DangerZone.path = "/danger-zone";
