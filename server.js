const express = require('express');
    const app = express();
    const port = 3000;

    // Set up EJS for templating
    app.set('view engine', 'ejs');
    app.use(express.urlencoded({ extended: true }));

    // Serve static files
    app.use(express.static('public'));

    // Main route
    app.get('/', (req, res) => {
      res.render('index', { result: null });
    });

    // Form submission route
    app.post('/generate', (req, res) => {
      const { topic } = req.body;
      
      // Simulate content generation
      const result = {
        status: 'success',
        content: {
          title: `Exploring ${topic}`,
          sections: [
            "Introduction to the topic",
            "Current trends and developments",
            "Future outlook"
          ]
        }
      };

      res.render('index', { result });
    });

    app.listen(port, () => {
      console.log(`App running at http://localhost:${port}`);
    });
