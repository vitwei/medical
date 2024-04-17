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
      title: "Action confirmation",
      body: "You're about to delete all things. This action cannot be undone.",
      okText: "Proceed",
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
      'Reset Cache may help in cases like if you are unable to modify the labeling configuration due ' +
      'to validation errors concerning existing labels, but you are confident that the labels don\'t exist. You can ' +
      'use this action to reset the cache and try again.',
    label: `重置缓存`,
  }, {
    type: 'tabs',
    help: 'If the Data Manager is not loading, dropping all Data Manager tabs can help.',
    label: `删除所有页签`,
  }, {
    type: 'project',
    help: 'Deleting a project removes all tasks, annotations, and project data from the database.',
    label: '删除该项目',
  }], [project]);

  return (
    <div style={{ width: 480 }}>
      <Label
        text="Delete Annotations, Tasks, or Project"
        description="Perform these actions at your own risk. Actions you take on this page can't be reverted. Make sure your data is backed up."
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
