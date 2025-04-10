import { useState } from 'react'
import axios from 'axios'
import { Container, Typography, TextField, Button, Paper, Box, CircularProgress, AppBar, Toolbar } from '@mui/material'
import AnalyzeIcon from '@mui/icons-material/Search'
import ReactMarkdown from 'react-markdown'
import './App.css'

function App() {
  const [url, setUrl] = useState('')
  const [analysis, setAnalysis] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleAnalyze = async () => {
    if (!url) {
      setError('Please enter a URL')
      return
    }

    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      setError('URL must start with http:// or https://')
      return
    }

    setLoading(true)
    setError('')
    setAnalysis('')

    try {
      const apiUrl = import.meta.env.VITE_API_BASE_URL || '/api';
      const response = await axios.post(`${apiUrl}/analyze`, { url })
      if (response.data.success) {
        setAnalysis(response.data.analysis)
      } else {
        setError(response.data.error || 'Failed to analyze the URL')
      }
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'An error occurred while analyzing the URL')
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <AppBar position="static" color="primary" sx={{ mb: 4 }}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Web Analyser
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg">
        <Box sx={{ my: 4 }}>
          <Typography variant="h4" component="h1" align="center" gutterBottom>
            Analyse Any Web Page
          </Typography>
          <Typography variant="subtitle1" align="center" color="text.secondary" paragraph>
            Enter a URL to analyse and get a detailed summary of the web page content.
          </Typography>

          <Box sx={{ display: 'flex', alignItems: 'center', mt: 4, mb: 2 }}>
            <TextField
              fullWidth
              label="Enter URL"
              variant="outlined"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              error={!!error}
              helperText={error}
              placeholder="https://example.com"
              sx={{ mr: 2 }}
            />
            <Button
              variant="contained"
              color="primary"
              size="large"
              onClick={handleAnalyze}
              disabled={loading}
              startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <AnalyzeIcon />}
            >
              {loading ? 'Analysing...' : 'Analyse'}
            </Button>
          </Box>

          {loading && (
            <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
              <CircularProgress />
              <Typography variant="body1" sx={{ ml: 2 }}>
                Analysing web page... This may take a minute.
              </Typography>
            </Box>
          )}

          {analysis && (
            <Paper elevation={3} sx={{ p: 3, mt: 4 }}>
              <Typography variant="h5" gutterBottom>
                Analyse Results
              </Typography>
              <Box sx={{ mt: 2, overflow: 'auto', fontFamily: 'system-ui, sans-serif' }}>
                <ReactMarkdown>{analysis}</ReactMarkdown>
              </Box>
            </Paper>
          )}
        </Box>
      </Container>
    </>
  )
}

export default App
