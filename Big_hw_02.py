from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

app = Flask(__name__)
app.debug = True

def load_data():
    files = {
        'hw-01': 'Python-2025-hw-01-git.csv',
        'hw-02': 'Python-2025-hw-02-data-types.csv',
        'big-hw-01': 'Python-2025-big-hw-01.csv'
    }
    
    dfs = []
    for hw_name, filename in files.items():
        if os.path.exists(filename):
            df = pd.read_csv(filename, header=None, names=['name', 'group_id', 'col2', 'score'])
            df['hw_name'] = hw_name
            dfs.append(df)
    
    if not dfs:
        return pd.DataFrame()
    
    return pd.concat(dfs, ignore_index=True)

df = load_data()

def compute_mark(score):
    if pd.isna(score) or score == 0:
        return 2
    elif 1 <= score < 50:
        return 4
    else:
        return 5


@app.route('/names')
def names():
    unique_names = df['name'].dropna().unique().tolist()
    return jsonify(sorted(unique_names))

@app.route('/<hw_name>/mean_score')
def hw_mean_score(hw_name):
    if hw_name not in df['hw_name'].unique():
        return jsonify({'error': 'Homework not found'}), 404
    
    mean_score = df[df['hw_name'] == hw_name]['score'].mean()
    return jsonify({'mean_score': mean_score})

@app.route('/<hw_name>/<group_id>/mean_score')
def hw_group_mean_score(hw_name, group_id):
    filtered = df[(df['hw_name'] == hw_name) & (df['group_id'] == group_id)]
    if filtered.empty:
        return jsonify({'error': 'Data not found'}), 404
    
    mean_score = filtered['score'].mean()
    return jsonify({'mean_score': mean_score})

@app.route('/mean_score')
def mean_score_query():
    hw_name = request.args.get('hw_name')
    group_id = request.args.get('group_id')
    
    if not hw_name or not group_id:
        return jsonify({'error': 'Missing parameters'}), 400
    
    return hw_group_mean_score(hw_name, group_id)

@app.route('/mark')
def mark():
    name = request.args.get('name')
    group_id = request.args.get('group_id')
    
    if name:
        student_scores = df[df['name'] == name]['score']
        avg_score = student_scores.mean()
        return jsonify({'mark': compute_mark(avg_score)})
    elif group_id:
        group_scores = df[df['group_id'] == group_id]['score']
        avg_score = group_scores.mean()
        return jsonify({'mean_mark': compute_mark(avg_score)})
    else:
        return jsonify({'error': 'Missing parameters'}), 400

@app.route('/course_table')
def course_table():
    hw_name = request.args.get('hw_name')
    group_id = request.args.get('group_id')
    
    if not hw_name:
        return "Error 400", 400
    
    filtered = df[df['hw_name'] == hw_name]
    
    if group_id:
        filtered = filtered[filtered['group_id'] == group_id]
        if filtered.empty:
            return f"Error 404", 404
    else:
        if filtered.empty:
            return f"Error 404", 404
    
    result_df = filtered[['name', 'group_id', 'score']].copy()
    result_df['mark'] = result_df['score'].apply(compute_mark)
    result_df.sort_values(['group_id', 'name'], inplace=True)
    
    students = result_df.to_dict('records')
    groups = sorted(result_df['group_id'].unique().tolist())
    
    return render_template('course_table.html', 
                         students=students,
                         hw_name=hw_name,
                         group_id=group_id,
                         groups=groups)

if __name__ == '__main__':
    app.run(host='localhost', port=1337)