import { observer } from "mobx-react";
import React from "react";
import { FilterDropdown } from "../FilterDropdown";
// import { Common } from "./Common";

export const VariantSelect = observer(({ filter, schema, onChange, multiple, value }) => {
  if (!schema) return <></>;
  const { items } = schema;

  const selectedValue = (() => {
    if (!multiple) {
      return Array.isArray(value) ? value[0] : value;
    } else {
      return Array.isArray(value) ? value : value ?? [];
    }
  })();

  const FilterItem = filter.cellView?.FilterItem;

  return (
    <FilterDropdown
      items={items}
      value={selectedValue}
      multiple={multiple}
      optionRender={FilterItem}
      outputFormat={multiple ? (value) => {
        return value ? [].concat(value) : [];
      } : undefined}
      onChange={(value) => onChange(value)}
    />
  );
});

export const ListFilter = [
  {
    key: "contains",
    label: "包含",
    valueType: "single",
    input: (props) => <VariantSelect {...props} multiple/>,
  },
  {
    key: "not_contains",
    label: "不包含",
    valueType: "single",
    input: (props) => <VariantSelect {...props} multiple/>,
  },
  // ... Common,
];
