import React from 'react';
import ReactDOM from 'react-dom';
import { AppContainer } from 'react-hot-loader'; // required

import App from './containers/App/App';

import './index.scss';

const features = [
  {
    name: 'CtrlP',
    identifier: 'ctrlp',
    feature_type: 'Plugin',
    description: 'Full path fuzzy file, buffer, mru, tag, ... finder for Vim.',
    enabled: false,
    selected: false,
    visible: true,
    category: 'Navigation',
    installed: true,
    template: 'ctrlp.j2',
    vundle_installation: 'ctrlpvim/ctrlp.vim',
    options:
    [
      {
        name: 'CtrlP Command',
        identifier: 'ctrlp_cmd',
        option_type: 'Choice',
        options: ['CtrlPMixed', 'CtrlPStam', 'CtrlPDrek'],
        pretty_name: 'CtrlP Command',
        description: 'Which mode should CtrlP start in',
        default_value: 'CtrlPMixed',
      },
      {
        name: 'CtrlP Extensions',
        identifier: 'ctrlp_extensions',
        option_type: 'MultipleSelection',
        pretty_name: 'CtrlP Extensions',
        description: 'Select which CtrlP extensions to enable',
        default_value: ['dir', 'mixed'],
        options: ['tag', 'buffertag', 'quickfix', 'dir', 'rtscript', 'undo', 'line', 'changes', 'mixed', 'bookmarkdir'],
      },
      {
        name: 'CtrlP working path mode',
        identifier: 'ctrlp_working_path_mode',
        option_type: 'MultipleSelection',
        options: ['c', 'a', 'r', 'w', '0'],
        pretty_name: 'CtrlP working path mode',
        description: 'How should CtrlP choose its working directory when starting?',
        details: 'c - the directory of the current file.\na - like "c", but only applies when the current working directory outside of CtrlP isn\'t a direct ancestor of the directory of the current file.\nr - the nearest ancestor that contains one of these directories or files: .git .hg .svn .bzr _darcs\nw - begin finding a root from the current working directory outside of CtrlP instead of from the directory of the current file (default). Only applies when "r" is also present.\n 0 or <empty> - disable this feature.',
        default_value: 'r',
      },
    ],
  },
  {
    name: 'Tagbar',
    description: 'Tag browser',
    selected: false,
    visible: true,
  },
  {
    name: 'Disable arrow keys',
    description: 'Disable arrow keys, helps you learn to use just hjkl',
    selected: false,
    visible: true,
  },
  {
    name: 'Highlight search',
    description: 'Highlight search results',
    selected: false,
    visible: true,
  },
];

function renderApp() {
  // We now render `<AppContainer>` instead of our App component.
  ReactDOM.render(
    <AppContainer>
      <App features={features} />
    </AppContainer>,
    document.getElementById('main'),
  );
}

renderApp(); // Renders App on init

if (module.hot) {
  // Renders App every time a change in code happens.
  module.hot.accept('./containers/App/App.jsx', renderApp);
}
