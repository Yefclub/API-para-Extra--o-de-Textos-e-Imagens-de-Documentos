from flask import Blueprint, jsonify, request
from src.models.user import User, db

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    """Lista todos os usuários"""
    try:
        users = User.query.all()
        return jsonify({
            'success': True,
            'users': [user.to_dict() for user in users],
            'total': len(users)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@user_bp.route('/users', methods=['POST'])
def create_user():
    """Cria um novo usuário"""
    try:
        data = request.json
        
        if not data or 'username' not in data or 'email' not in data:
            return jsonify({
                'success': False,
                'error': 'Username e email são obrigatórios'
            }), 400
        
        # Verificar se usuário já existe
        existing_user = User.query.filter(
            (User.username == data['username']) | (User.email == data['email'])
        ).first()
        
        if existing_user:
            return jsonify({
                'success': False,
                'error': 'Usuário ou email já existem'
            }), 409
        
        user = User(username=data['username'], email=data['email'])
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Obtém um usuário específico"""
    try:
        user = User.query.get_or_404(user_id)
        return jsonify({
            'success': True,
            'user': user.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Atualiza um usuário"""
    try:
        user = User.query.get_or_404(user_id)
        data = request.json
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Dados não fornecidos'
            }), 400
        
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'user': user.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Remove um usuário"""
    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Usuário removido com sucesso'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 