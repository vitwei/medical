import React, { Fragment } from 'react';
import { observer } from 'mobx-react';
import { types } from 'mobx-state-tree';

import BaseTool from './Base';
import ToolMixin from '../mixins/Tool';
import { Tool } from '../components/Toolbar/Tool';
import { FlyoutMenu } from '../components/Toolbar/FlyoutMenu';
import { IconExpand, IconHandTool, IconZoomIn, IconZoomOut } from '../assets/icons';

const ToolView = observer(({ item }) => {
  return (
    <Fragment>
      <Tool
        active={item.selected}
        icon={<IconHandTool />}
        ariaLabel="pan"
        label="平移图像"
        shortcut="H"
        onClick={() => {
          const sel = item.selected;

          item.manager.selectTool(item, !sel);
        }}
      />
      <Tool
        icon={<IconZoomIn />}
        ariaLabel="zoom-in"
        label="放大"
        shortcut="ctrl+plus"
        onClick={() => {
          item.handleZoom(1);
        }}
      />
      <FlyoutMenu
        icon={<IconExpand />}
        items={[
          {
            label: '缩放到合适尺寸',
            shortcut: 'shift+1',
            onClick: () => {
              item.sizeToFit();
            },
          },
          {
            label: '缩放到原始尺寸',
            shortcut: 'shift+2',
            onClick: () => {
              item.sizeToOriginal();
            },
          },
        ]}
      />
      <Tool
        icon={<IconZoomOut />}
        ariaLabel="zoom-out"
        label="缩小"
        shortcut="ctrl+minus"
        onClick={() => {
          item.handleZoom(-1);
        }}
      />
    </Fragment>
  );
});

const _Tool = types
  .model('ZoomPanTool', {
    // image: types.late(() => types.safeReference(Registry.getModelByTag("image")))
    group: 'control',
  })
  .volatile(() => ({
    canInteractWithRegions: false,
  }))
  .views(self => ({
    get viewClass() {
      return () => <ToolView item={self} />;
    },

    get stageContainer() {
      return self.obj.stageRef.container();
    },
  }))
  .actions(self => ({
    shouldSkipInteractions() {
      return true;
    },

    mouseupEv() {
      self.mode = 'viewing';
      self.stageContainer.style.cursor = 'grab';
    },

    updateCursor() {
      if (!self.selected || !self.obj?.stageRef) return;

      self.stageContainer.style.cursor = 'grab';
    },

    afterUpdateSelected() {
      self.updateCursor();
    },

    handleDrag(ev) {
      const item = self.obj;
      const posx = item.zoomingPositionX + ev.movementX;
      const posy = item.zoomingPositionY + ev.movementY;

      item.setZoomPosition(posx, posy);
    },

    mousemoveEv(ev) {
      const zoomScale = self.obj.zoomScale;

      if (zoomScale <= 1) return;
      if (self.mode === 'moving') {
        self.handleDrag(ev);
        self.stageContainer.style.cursor = 'grabbing';
      }
    },

    mousedownEv(ev) {
      // don't pan on right click
      if (ev.button === 2) return;

      self.mode = 'moving';
      self.stageContainer.style.cursor = 'grabbing';
    },

    handleZoom(val) {
      const item = self.obj;

      item.handleZoom(val);
    },

    sizeToFit() {
      const item = self.obj;

      item.sizeToFit();
    },

    sizeToAuto() {
      const item = self.obj;

      item.sizeToAuto();
    },

    sizeToOriginal() {
      const item = self.obj;

      item.sizeToOriginal();
    },
  }));

const Zoom = types.compose(_Tool.name, ToolMixin, BaseTool, _Tool);

export { Zoom };
