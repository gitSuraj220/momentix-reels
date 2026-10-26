import React from 'react';
import {Composition} from 'remotion';
import {StyleFrame} from './scenes/StyleFrame';
export const Root: React.FC = () => (
  <>
    <Composition id="SF" component={StyleFrame} width={1080} height={1920} fps={30} durationInFrames={60} defaultProps={{beat: 1}} />
  </>
);
