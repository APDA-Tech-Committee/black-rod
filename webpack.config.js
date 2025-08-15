const path = require("path");
const webpack = require("webpack");
const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  context: __dirname,
  entry: "./apda/assets/js/index",

  output: {
    path: path.resolve("./apda/assets/webpack_bundles/"),
    filename: "[name]-[fullhash].js",
    publicPath: "/static/webpack_bundles/",
  },

  plugins: [
  new BundleTracker({
  path: path.resolve(__dirname, 'apda/apda/assets/webpack_bundles'),
  filename: 'webpack-stats.json',
  logTime: true
})
,
  new webpack.ProvidePlugin({
    $: "jquery",
    Popper: "popper.js"
  })
],


    module: {
        rules: [
            {
                test: /\.css$/,
                use: [
                    "style-loader",
                    "css-loader"
                ],
            },
            {
                test: /\.(less)$/,
                use: [
                    "style-loader", 
                    "css-loader",  
                    "less-loader", 
                ],
            },
            {
                test: /\.(scss)$/,
                use: [
                    "style-loader",
                    "css-loader",
                    {
					loader: 'postcss-loader',
					options: {
						postcssOptions: {
						plugins: [
							require('precss'),
							require('autoprefixer')
						]
						}
					}
					},
                    {
                        loader: "sass-loader",
                        options: {
                            implementation: require("sass"), 
                        },
                    },
                ],
            },
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: ["babel-loader"],
            },
        ],
    },

    resolve: {
        extensions: ["*", ".js", ".jsx"],
    },
};
