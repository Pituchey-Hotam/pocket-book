import React, { useState } from 'react';
import { Button, FormControl, FormLabel, Grid, Switch, TextField } from '@mui/material';

const App = () => {
  const [file, setFile] = useState('');
  const [numberOfPages, setNumberOfPages] = useState('');
  const [pagesPerSheet, setPagesPerSheet] = useState('');
  const [isGluing, setIsGluing] = useState(true);
  const [isOneNotebook, setIsOneNotebook] = useState(true);
  const [isEnglish, setIsEnglish] = useState(true);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    setFile(selectedFile);
  };

  const handleSubmit = () => {
    // Perform the necessary operations with the provided inputs
    // ...
  };

  const handleLanguageChange = () => {
    setIsEnglish((prevState) => !prevState);
  };

  const language = isEnglish ? 'English' : 'עברית';

  return (
    <Grid container spacing={2}>
      <Grid item xs={12}>
        <Button variant="contained" onClick={handleLanguageChange}>
          {language}
        </Button>
      </Grid>
      <Grid item xs={12}>
        <FormControl fullWidth>
          <FormLabel>{isEnglish ? 'Choose a file:' : 'בחר קובץ:'}</FormLabel>
          <input type="file" onChange={handleFileChange} />
        </FormControl>
      </Grid>
      <Grid item xs={12} sm={6}>
        <FormControl fullWidth>
          <FormLabel>
            {isEnglish
              ? 'Enter number of pages in each booklet (In multiples of 4. the standard is 32):'
              : 'הכנס מספר העמודים בכל מחברת (בכפולות של 4, הסטנדרט הוא 32):'}
          </FormLabel>
          <TextField type="text" size="small" value={numberOfPages} onChange={(e) => setNumberOfPages(e.target.value)} />
        </FormControl>
      </Grid>
      <Grid item xs={12} sm={6}>
        <FormControl fullWidth>
          <FormLabel>
            {isEnglish ? 'Enter pages per sheet (2/4/8/16):' : 'הכנס מספר עמודים לעמוד (2/4/8/16):'}
          </FormLabel>
          <TextField type="text" size="small" value={pagesPerSheet} onChange={(e) => setPagesPerSheet(e.target.value)} />
        </FormControl>
      </Grid>
      <Grid item xs={12}>
        <FormControl component="fieldset">
          <FormLabel>
            {isEnglish ? 'Sewing or gluing? In the gluing there is an extra blank page on each side.' : 'מודבק או תפור? בגרסא המודבקת יש תוספת של עמוד ריק בכל מחברת:'}
          </FormLabel>
          <Switch checked={isGluing} onChange={() => setIsGluing((prevState) => !prevState)} />
          <span>
            {isGluing ? (isEnglish ? 'Gluing' : 'מודבק') : (isEnglish ? 'Sewing' : 'תפור')}
          </span>
        </FormControl>
      </Grid>
      <Grid item xs={12}>
        <FormControl component="fieldset">
          <FormLabel>
            {isEnglish ? 'Only one notebook?' : 'האם כבודו מדפיס רק מחברת אחת?'}
          </FormLabel>
          <Switch checked={isOneNotebook} onChange={() => setIsOneNotebook((prevState) => !prevState)} />
          <span>
            {isOneNotebook ? (isEnglish ? 'Yes' : 'כן') : (isEnglish ? 'No' : 'לא')}
          </span>
        </FormControl>
      </Grid>
      <Grid item xs={12}>
        <Button variant="contained" onClick={handleSubmit}>
          {isEnglish ? 'Do it' : 'יאללה לעבודה'}
        </Button>
      </Grid>
    </Grid>
  );
};

export default App;
