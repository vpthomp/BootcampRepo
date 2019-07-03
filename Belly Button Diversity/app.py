{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "\n",
    "from sqlalchemy.ext.automap import automap_base\n",
    "from sqlalchemy.orm import Session\n",
    "from sqlalchemy import create_engine\n",
    "\n",
    "from flask import Flask, jsonify, render_template\n",
    "from flask_sqlalchemy import SQLAlchemy"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {},
   "outputs": [],
   "source": [
    "app = Flask(__name__)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\bob\\Anaconda3\\envs\\pythondata\\lib\\site-packages\\flask_sqlalchemy\\__init__.py:835: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.\n",
      "  'SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and '\n"
     ]
    }
   ],
   "source": [
    "#################################################\n",
    "# Database Setup\n",
    "#################################################\n",
    "\n",
    "app.config[\"SQLALCHEMY_DATABASE_URI\"] = \"sqlite:///db/bellybutton.sqlite\"\n",
    "db = SQLAlchemy(app)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "metadata": {},
   "outputs": [],
   "source": [
    "# reflect an existing database into a new model\n",
    "Base = automap_base()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {},
   "outputs": [],
   "source": [
    "# reflect the tables\n",
    "Base.prepare(db.engine, reflect=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "metadata": {},
   "outputs": [
    {
     "ename": "AttributeError",
     "evalue": "sample_metadata",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mKeyError\u001b[0m                                  Traceback (most recent call last)",
      "\u001b[1;32m~\\Anaconda3\\envs\\pythondata\\lib\\site-packages\\sqlalchemy\\util\\_collections.py\u001b[0m in \u001b[0;36m__getattr__\u001b[1;34m(self, key)\u001b[0m\n\u001b[0;32m    209\u001b[0m         \u001b[1;32mtry\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m--> 210\u001b[1;33m             \u001b[1;32mreturn\u001b[0m \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_data\u001b[0m\u001b[1;33m[\u001b[0m\u001b[0mkey\u001b[0m\u001b[1;33m]\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m    211\u001b[0m         \u001b[1;32mexcept\u001b[0m \u001b[0mKeyError\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;31mKeyError\u001b[0m: 'sample_metadata'",
      "\nDuring handling of the above exception, another exception occurred:\n",
      "\u001b[1;31mAttributeError\u001b[0m                            Traceback (most recent call last)",
      "\u001b[1;32m<ipython-input-28-c271297765c9>\u001b[0m in \u001b[0;36m<module>\u001b[1;34m\u001b[0m\n\u001b[0;32m      1\u001b[0m \u001b[1;31m# Save references to each table\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m----> 2\u001b[1;33m \u001b[0mSamples_Metadata\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mBase\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mclasses\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0msample_metadata\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m      3\u001b[0m \u001b[0mSamples\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mBase\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mclasses\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0msamples\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\Anaconda3\\envs\\pythondata\\lib\\site-packages\\sqlalchemy\\util\\_collections.py\u001b[0m in \u001b[0;36m__getattr__\u001b[1;34m(self, key)\u001b[0m\n\u001b[0;32m    210\u001b[0m             \u001b[1;32mreturn\u001b[0m \u001b[0mself\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0m_data\u001b[0m\u001b[1;33m[\u001b[0m\u001b[0mkey\u001b[0m\u001b[1;33m]\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    211\u001b[0m         \u001b[1;32mexcept\u001b[0m \u001b[0mKeyError\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m--> 212\u001b[1;33m             \u001b[1;32mraise\u001b[0m \u001b[0mAttributeError\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mkey\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m    213\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    214\u001b[0m     \u001b[1;32mdef\u001b[0m \u001b[0m__contains__\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mself\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mkey\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;31mAttributeError\u001b[0m: sample_metadata"
     ]
    }
   ],
   "source": [
    "# Save references to each table\n",
    "Samples_Metadata = Base.classes.sample_metadata\n",
    "Samples = Base.classes.samples"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/\")\n",
    "def index():\n",
    "    \"\"\"Return the homepage.\"\"\"\n",
    "    return render_template(\"index.html\")\n",
    "\n",
    "\n",
    "@app.route(\"/names\")\n",
    "def names():\n",
    "    \"\"\"Return a list of sample names.\"\"\"\n",
    "\n",
    "    # Use Pandas to perform the sql query\n",
    "    stmt = db.session.query(Samples).statement\n",
    "    df = pd.read_sql_query(stmt, db.session.bind)\n",
    "\n",
    "    # Return a list of the column names (sample names)\n",
    "    return jsonify(list(df.columns)[2:])\n",
    "\n",
    "\n",
    "@app.route(\"/metadata/<sample>\")\n",
    "def sample_metadata(sample):\n",
    "    \"\"\"Return the MetaData for a given sample.\"\"\"\n",
    "    sel = [\n",
    "        Samples_Metadata.sample,\n",
    "        Samples_Metadata.ETHNICITY,\n",
    "        Samples_Metadata.GENDER,\n",
    "        Samples_Metadata.AGE,\n",
    "        Samples_Metadata.LOCATION,\n",
    "        Samples_Metadata.BBTYPE,\n",
    "        Samples_Metadata.WFREQ,\n",
    "    ]\n",
    "\n",
    "    results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()\n",
    "\n",
    "    # Create a dictionary entry for each row of metadata information\n",
    "    sample_metadata = {}\n",
    "    for result in results:\n",
    "        sample_metadata[\"sample\"] = result[0]\n",
    "        sample_metadata[\"ETHNICITY\"] = result[1]\n",
    "        sample_metadata[\"GENDER\"] = result[2]\n",
    "        sample_metadata[\"AGE\"] = result[3]\n",
    "        sample_metadata[\"LOCATION\"] = result[4]\n",
    "        sample_metadata[\"BBTYPE\"] = result[5]\n",
    "        sample_metadata[\"WFREQ\"] = result[6]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
