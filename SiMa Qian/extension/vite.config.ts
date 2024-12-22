// @ts-ignore
const config = {
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: {
        popup: './src/popup.tsx',
        options: './src/options.tsx',
        content: './content.js',
        background: './background.js',
        style: './content.css'
      },
      output: {
        format: 'es',
        entryFileNames: '[name].js',
        chunkFileNames: '[name].[hash].js',
        assetFileNames: '[name].[ext]',
        globals: {
          'react': 'React',
          'react-dom': 'ReactDOM',
          '@headlessui/react': 'Headless',
          'langchain': 'LangChain'
        }
      },
      external: [
        'react',
        'react-dom',
        '@headlessui/react',
        'langchain'
      ]
    }
  },
  server: {
    port: 3000,
    open: false
  },
  optimizeDeps: {
    exclude: ['react', 'react-dom', '@headlessui/react', 'langchain']
  },
  plugins: [{
    name: 'html-transform',
    transformIndexHtml(html) {
      return {
        html,
        tags: [
          {
            tag: 'script',
            attrs: {
              src: 'https://cdn.jsdelivr.net/npm/react@18/umd/react.production.min.js',
              crossorigin: 'anonymous'
            },
            injectTo: 'head'
          },
          {
            tag: 'script',
            attrs: {
              src: 'https://cdn.jsdelivr.net/npm/react-dom@18/umd/react-dom.production.min.js',
              crossorigin: 'anonymous'
            },
            injectTo: 'head'
          },
          {
            tag: 'script',
            attrs: {
              src: 'https://cdn.jsdelivr.net/npm/@headlessui/react@1.7.17/dist/index.umd.js',
              crossorigin: 'anonymous'
            },
            injectTo: 'head'
          },
          {
            tag: 'script',
            attrs: {
              src: 'https://cdn.jsdelivr.net/npm/langchain@0.0.197/dist/index.min.js',
              crossorigin: 'anonymous'
            },
            injectTo: 'head'
          }
        ]
      }
    }
  }]
};

export default config; 