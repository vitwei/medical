import { observer } from 'mobx-react';
import React from 'react';
import { FilterInput } from '../FilterInput';
import { Common } from './Common';

const BaseInput = observer((props) => {
  return (
    <FilterInput
      {...props}
      type='text'
      value={props.value}
      onChange={props.onChange}
      style={{ fontSize: 14 }}
      placeholder={props.placeholder}
    />
  );
});

export const StringFilter = [
  {
    key: 'contains',
    label: '包含',
    valueType: 'single',
    input: BaseInput,
  },
  {
    key: 'not_contains',
    label: '不包含',
    valueType: 'single',
    input: BaseInput,
  },
  {
    key: 'regex',
    label: '正则式',
    valueType: 'single',
    input: BaseInput,
  },
  {
    key: 'equal',
    label: '等于',
    valueType: 'single',
    input: BaseInput,
  },
  {
    key: 'not_equal',
    label: '不等于',
    valueType: 'single',
    input: BaseInput,
  },
  ...Common,
];
