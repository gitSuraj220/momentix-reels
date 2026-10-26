import React from 'react';
import {Composition} from 'remotion';
import {StyleFrame} from './scenes/StyleFrame';
import {Film, TOTAL} from './scenes/Film';
export const Root: React.FC = () => (
  <>
    <Composition id="SF" component={StyleFrame} width={1080} height={1920} fps={30} durationInFrames={60} defaultProps={{beat: 1}} />
    <Composition id="Film" component={Film} width={1080} height={1920} fps={30} durationInFrames={TOTAL} defaultProps={{captions: true, audio: false}} />
  </>
);
