import { useMemo } from 'react';
import { Menu } from "../Menu/Menu";

export const TabsMenu = ({
  onClick,
  editable = true,
  closable = true,
  clonable = true,
  virtual = false,
}) => {
  const items = useMemo(() => [{
    key: 'edit',
    title: '重命名',
    enabled: editable && !virtual,
    action: () => onClick("edit"),
  }, {
    key: 'duplicate',
    title: '复制',
    enabled: !virtual && clonable,
    action: () => onClick("duplicate"),
  }, {
    key: 'save',
    title: '保存',
    enabled: virtual,
    action: () => onClick("save"),
  }], [editable, closable, clonable, virtual]);

  const showDivider = useMemo(() => closable && items.some(({ enabled }) => enabled), [items]);

  return (
    <Menu size="medium" onClick={(e) => e.domEvent.stopPropagation()}>
      {items.map((item) => item.enabled ? (
        <Menu.Item key={item.key} onClick={item.action}>
          {item.title}
        </Menu.Item>
      ) : null)}

      {closable ? (
        <>
          {showDivider && <Menu.Divider />}
          <Menu.Item onClick={() => onClick("close")}>
            关闭
          </Menu.Item>
        </>
      ) : null}
    </Menu>
  );
};
