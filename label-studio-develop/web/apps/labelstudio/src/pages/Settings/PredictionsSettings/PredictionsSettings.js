import { useCallback, useContext, useEffect, useState } from 'react';
import { Description } from '../../../components/Description/Description';
import { Divider } from '../../../components/Divider/Divider';
import { EmptyState } from '../../../components/EmptyState/EmptyState';
import { Caption } from '../../../components/Caption/Caption';
import { IconEmptyPredictions } from '../../../assets/icons';
import { useAPI } from '../../../providers/ApiProvider';
import { ProjectContext } from '../../../providers/ProjectProvider';
import { Spinner } from '../../../components/Spinner/Spinner';
import { PredictionsList } from './PredictionsList';
import { Block, Elem } from '../../../utils/bem';
import { Label } from "../../../components/Form";
import './PredictionsSettings.styl';

export const PredictionsSettings = () => {
  const api = useAPI();
  const { project } = useContext(ProjectContext);
  const [versions, setVersions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loaded, setLoaded] = useState(false);

  const fetchVersions = useCallback(async () => {
    setLoading(true);
    const versions = await api.callApi('projectModelVersions', {
      params: {
        pk: project.id,
        extended: true,
      },
    });

    if (versions) setVersions(versions.static);
    setLoading(false);
    setLoaded(true);
  }, [project, setVersions]);

  useEffect(() => {
    if (project.id) {
      fetchVersions();
    }
  }, [project]);

  return (
    <Block name="prediction-settings">
      <Elem name={'wrapper'}>
        {loading && <Spinner size={32} />}

        {loaded && versions.length > 0 && (
          <Elem name="title-block">
            <Elem name="title">Predictions List</Elem>
            <Description  style={{ marginTop: '1em' }}>
              List of predictions available in the project.
              Each card is associated with a separate model version.
              To learn about how to import predictions,{' '}
                <a
                  href="https://labelstud.io/guide/predictions.html"
                  target="_blank"
                  rel="noreferrer"
                >see&nbsp;the&nbsp;documentation</a>.
            </Description>
          </Elem>
        )}

        {loaded && versions.length === 0 && (
          <EmptyState
            icon={<IconEmptyPredictions />}
            title="尚未上传预测"
            description="预测可以用于预先标记数据或验证模型。您可以从多个模型版本上传和选择预测。也可以在“模型”选项卡中连接活动模型。"
          />
        )}

        <PredictionsList
          project={project}
          versions={versions}
          fetchVersions={fetchVersions}
        />

        <Divider height={32} />
      </Elem>
    </Block>
  );
};

PredictionsSettings.title = '预测';
PredictionsSettings.path = '/predictions';
