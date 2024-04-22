import React from 'react';
import { Columns } from '../../../components/Columns/Columns';
import { Description } from '../../../components/Description/Description';
import { Block, cn } from '../../../utils/bem';
import { StorageSet } from './StorageSet';
import './StorageSettings.styl';
import { isInLicense, LF_CLOUD_STORAGE_FOR_MANAGERS } from '../../../utils/license-flags';

const isAllowCloudStorage = !isInLicense(LF_CLOUD_STORAGE_FOR_MANAGERS);

export const StorageSettings = () => {
  const rootClass = cn("storage-settings");

  return isAllowCloudStorage ? (
    <Block name="storage-settings">
      <Description style={{ marginTop: 0 }}>
      使用云或数据库存储作为标记任务的源文件或已完成注释的目标
      </Description>

      <Columns count={2} gap="40px" size="320px" className={rootClass}>
        <StorageSet
          title="文件云储存"
          buttonLabel="添加存储"
          rootClass={rootClass}
        />

        <StorageSet
          title="标注存储"
          target="export"
          buttonLabel="添加标注存储"
          rootClass={rootClass}
        />
      </Columns>
    </Block>
  ) : null;
};

StorageSettings.title = "云储存";
StorageSettings.path = "/storage";
