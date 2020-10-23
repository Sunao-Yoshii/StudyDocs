// Find the full example of all available configuration options at
// https://github.com/muenzpraeger/create-lwc-app/blob/main/packages/lwc-services/example/lwc-services.config.js
module.exports = {
    resources: [
        { from: 'src/client/resources/', to: 'dist/resources/' },
        { from: 'node_modules/bootstrap/dist', to: 'src/bootstrap' },
        { from: 'node_modules/bootstrap/dist', to: 'dist/bootstrap' },
        { from: 'node_modules/jquery/dist', to: 'src/jquery' },
        { from: 'node_modules/jquery/dist', to: 'dist/jquery' }
    ],

    sourceDir: './src/client',

    devServer: {
        proxy: { '/': 'http://localhost:3002' }
    }
};
