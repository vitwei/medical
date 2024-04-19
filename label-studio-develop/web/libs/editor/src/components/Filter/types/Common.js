import React from 'react';
import { FilterDropdown } from '../FilterDropdown';
import { observer } from 'mobx-react';


const BaseInput = observer((props) => (
  <FilterDropdown
    onChange={(value) => props.onChange(value)}
    items={[
      { label: '是' },
      { label: '否' },
    ]}
  />
));

export const Common = [
  {
    key: 'empty',
    label: '为空',
    input: BaseInput,
  },
];
