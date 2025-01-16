const express = require('express');
    const { createClient } = require('@supabase/supabase-js');
    const OpenAI = require('openai');

    const app = express();
    app.use(express.json());

    // Initialize clients
    const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY);
    const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

    // Blog generation endpoint
    app.post('/generate-blog', async (req, res) => {
      try {
        const { topic } = req.body;
        
        // Generate outline
        const outline = await openai.chat.completions.create({
          model: "gpt-4",
          messages: [{
            role: "system",
            content: "You are a content director. Create blog outlines based on topics."
          }, {
            role: "user",
            content: `Create outline for: ${topic}`
          }]
        });

        // Save to Supabase
        const { data, error } = await supabase
          .from('blog_posts')
          .insert([{ topic, outline: outline.choices[0].message.content }]);

        if (error) throw error;

        res.json({ success: true, data });
      } catch (error) {
        res.status(500).json({ error: error.message });
      }
    });

    const PORT = process.env.PORT || 3000;
    app.listen(PORT, () => {
      console.log(`Server running on port ${PORT}`);
    });
