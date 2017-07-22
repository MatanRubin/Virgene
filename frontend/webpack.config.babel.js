import path from 'path';
import HtmlWebpackPlugin from 'html-webpack-plugin';
import { NamedModulesPlugin, HotModuleReplacementPlugin } from 'webpack';

const ExtractTextPlugin = require('extract-text-webpack-plugin');

export default () => ({
  entry: [
    'react-hot-loader/patch', // Needed to preserve state
    'webpack-dev-server/client?http://localhost:8080', // webpack dev server host and port
    path.join(__dirname, 'src/index.jsx'),
  ],
  output: {
    path: path.join(__dirname, 'dist'),
    filename: 'bundle.js',
  },
  plugins: [
    new ExtractTextPlugin('style.css'),
    new HtmlWebpackPlugin({
      filename: 'index.html',
      template: './src/index.html',
    }),
    new HotModuleReplacementPlugin(), // Globally enable hot code replacement
    new NamedModulesPlugin(),
  ],
  devServer: {
    hot: true,
  },
  resolve: {
    extensions: ['.webpack.js', '.web.js', '.js', '.json', '.jsx'],
  },
  module: {
    rules: [
      {
        test: /.jsx?$/,
        exclude: /node_modules/,
        include: path.join(__dirname, 'src'),
        use: [
          {
            loader: 'babel-loader',
            options: {
              babelrc: false,
              plugins: ['react-hot-loader/babel'],
              presets: [
                ['es2015', { modules: false }],
                'react',
              ],
            },
          },
        ],
      },
      {
        test: /\.scss$/,
        exclude: /node_modules/,
        use: ExtractTextPlugin.extract({
          fallback: 'style-loader',
          use: [
            {
              loader: 'css-loader',
              query: {
                modules: true,
                sourceMap: true,
                importLoaders: 2,
                localIdentName: '[name]__[local]___[hash:base64:5]',
              },
            },
            'sass-loader',
          ],
        }),
      },
    ],
  },
});
