import React from 'react';
import { renderToString } from 'react-dom/server';
import { BarChart, Bar, XAxis, YAxis, Cell } from 'recharts';

const data = [{ name: 'A', score: 95, sentiment: 'positive' }];

const html = renderToString(
  <BarChart width={100} height={100} data={data}>
    <XAxis dataKey="name" />
    <YAxis />
    <Bar dataKey="score">
      {data.map((entry, index) => <Cell key={index} fill="#ff0000" />)}
    </Bar>
  </BarChart>
);
console.log(html);
