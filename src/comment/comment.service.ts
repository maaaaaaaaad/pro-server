import { Injectable, InternalServerErrorException } from '@nestjs/common'
import { InjectRepository } from '@nestjs/typeorm'
import { CommentEntity } from './entities/comment.entity'
import { Repository } from 'typeorm'
import { CommentRegisterInputDto } from './dtos/comment.register.dto'
import { UserEntity } from '../auth/entities/user.entity'
import { ItemEntity } from '../item/entities/item.entity'
import { CommentsGetInputDto } from './dtos/comments.get.dto'
import { CommentsMyInputDto } from './dtos/comments.my.dto'

@Injectable()
export class CommentService {
  constructor(
    @InjectRepository(CommentEntity)
    private readonly comment: Repository<CommentEntity>,
    @InjectRepository(ItemEntity) private readonly item: Repository<ItemEntity>,
  ) {}

  async register(
    owner: UserEntity,
    { itemId, content }: CommentRegisterInputDto,
  ) {
    try {
      const item = await this.item.findOne({
        where: {
          pk: itemId,
        },
      })
      if (!item) {
        return {
          access: false,
          message: 'Not found item',
        }
      }
      const comment = await this.comment.create({
        content,
      })
      comment.owner = owner
      comment.item = item
      await this.comment.save(comment)
      return {
        access: true,
        message: 'Success register comment',
      }
    } catch (e) {
      throw new InternalServerErrorException(e.message)
    }
  }

  async getAll({ itemId, size, page }: CommentsGetInputDto) {
    try {
      const item = await this.item.findOne({
        where: {
          pk: itemId,
        },
      })
      if (!item) {
        return {
          access: false,
          message: 'Not found item',
        }
      }
      const [comments, commentsCount] = await this.comment.findAndCount({
        relations: ['owner'],
        where: {
          item: {
            pk: itemId,
          },
        },
        take: size,
        skip: (page - 1) * size,
        order: {
          createAt: 'DESC',
        },
      })
      return {
        access: true,
        message: 'Success',
        comments,
        pageCount: Math.ceil(commentsCount / size),
        commentsCount,
      }
    } catch (e) {
      throw new InternalServerErrorException(e.message)
    }
  }

  async getMy(owner: UserEntity, { size, page }: CommentsMyInputDto) {
    try {
      const [comments, commentsCount] = await this.comment.findAndCount({
        where: {
          owner: {
            pk: owner.pk,
          },
        },
        take: size,
        skip: (page - 1) * size,
        order: {
          createAt: 'DESC',
        },
      })
      return {
        access: true,
        message: 'Success',
        comments,
        pageCount: Math.ceil(commentsCount / size),
        commentsCount,
      }
    } catch (e) {
      throw new InternalServerErrorException(e.message)
    }
  }
}
