import { useCallback, useContext, useEffect, useRef, useState } from 'react';
import { Button } from '../../components';
import { Form, TextArea, Toggle } from '../../components/Form';
import { MenubarContext } from '../../components/Menubar/Menubar';
import { Block, Elem } from '../../utils/bem';

import { ModelVersionSelector } from './AnnotationSettings/ModelVersionSelector';
import { ProjectContext } from '../../providers/ProjectProvider';
import { Divider } from '../../components/Divider/Divider';

export const AnnotationSettings = () => {
  const { project, fetchProject } = useContext(ProjectContext);
  const pageContext = useContext(MenubarContext);
  const formRef = useRef();
  const [collab, setCollab] = useState(null);

  useEffect(() => {
    pageContext.setProps({ formRef });
  }, [formRef]);

  const updateProject = useCallback(() => {
    fetchProject(project.id, true);
  }, [project]);

  return (
    <Block name="annotation-settings">
      <Elem name={'wrapper'}>
        <Form
          ref={formRef}
          action="updateProject"
          formData={{ ...project }}
          params={{ pk: project.id }}
          onSubmit={updateProject}
        >
          <Form.Row columnCount={1}>
            <Elem name={'header'}>标注说明</Elem>
            <div>
              <Toggle label="在标注前显示" name="show_instruction" />
            </div>
            <div style={{ color: 'rgba(0,0,0,0.4)' }}>
              <p>编写说明以帮助用户完成标记任务</p>
              <p>
                指令字段支持HTML标记并允许使用
                images, iframes (pdf).
              </p>
            </div>
          </Form.Row>

          <Form.Row columnCount={1}>
            <TextArea
              name="expert_instruction"
              style={{ minHeight: 128, maxWidth: '520px' }}
            />
          </Form.Row>

          <Divider height={32} />

          <Form.Row columnCount={1} style={{ borderTop: '1px solid #f1f1f1' }}>
            <br />
            <Elem name={'header'}>实时预测</Elem>
            <div>
              <Toggle
                label="使用预测器预先标注任务"
                description={
                  <span>
                    启用并选择要用于预标记的预测集
                    Predictions will be pre-loaded in {" "}
                    <a
                      style={{ color: "rgb(105 129 185)" }}
                      target="_blank" href="https://labelstud.io/guide/labeling.html#Choose-which-tasks-to-label"
                    >Label&nbsp;All&nbsp;Tasks</a>{" "}
                    and {" "}
                    <a
                      style={{ color: "rgb(105 129 185)" }}
                      target="_blank" href="https://labelstud.io/guide/get_started#Interface"
                    >Quick View</a>.
                  </span>
                }
                name="show_collab_predictions"
                onChange={(e) => {
                  setCollab(e.target.checked);
                }}
              />
            </div>

            {(collab !== null ? collab : project.show_collab_predictions) && (
              <ModelVersionSelector />
            )}
          </Form.Row>

          <Form.Actions>
            <Form.Indicator>
              <span case="success">Saved!</span>
            </Form.Indicator>
            <Button type="submit" look="primary" style={{ width: 120 }}>
              Save
            </Button>
          </Form.Actions>
        </Form>
      </Elem>
    </Block>
  );
};

AnnotationSettings.title = '标注';
AnnotationSettings.path = '/annotation';
