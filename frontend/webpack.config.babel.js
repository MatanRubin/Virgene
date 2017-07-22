import path from 'path';
import HtmlWebpackPlugin from 'html-webpack-plugin';
import { HotModuleReplacementPlugin } from 'webpack';

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
    new HtmlWebpackPlugin({
      filename: 'index.html',
      template: './src/index.html',
    }),
    new HotModuleReplacementPlugin(), // Globally enable hot code replacement
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
        test: /\.(css|scss|sass)$/,
        loader: 'style-loader!css-loader!sass-loader',
      },
    ],
  },
});
